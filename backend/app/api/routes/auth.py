from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
import pyotp

from app.api.deps import get_current_user
from app.core.audit import audit_event
from app.core.auth import create_access_token, hash_password, verify_password
from app.core.database import get_db
from app.core.rate_limit import enforce_rate_limit, get_client_ip
from app.models.user import User
from app.schemas.auth import (
    AuthTokenResponse,
    LoginRequest,
    RegisterRequest,
    TwoFactorConfirmRequest,
    TwoFactorDisableRequest,
    TwoFactorSetupResponse,
    TwoFactorStatusResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(
    payload: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    email = payload.email.strip().lower()
    client_ip = get_client_ip(request)

    enforce_rate_limit(f"auth:register:ip:{client_ip}", limit=10, window_seconds=3600)
    enforce_rate_limit(f"auth:register:email:{email}", limit=3, window_seconds=3600)

    existing = db.execute(select(User).where(User.email == email).limit(1)).scalar_one_or_none()
    if existing:
        audit_event(
            event_type="auth.register.conflict",
            severity="warning",
            success=False,
            status_code=409,
            actor_type="anonymous",
            request=request,
            description="Register attempted with already registered email",
            details={"email": email},
        )
        raise HTTPException(status_code=409, detail="Email already registered")

    is_first_user = db.execute(select(User)).scalars().first() is None

    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        is_active=True,
        is_admin=is_first_user,
        two_factor_enabled=False,
        two_factor_secret=None,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    audit_event(
        event_type="auth.register.success",
        severity="info",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
        description="User registered successfully",
        details={"email": user.email, "is_admin": user.is_admin},
    )

    return UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/login", response_model=AuthTokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    email = payload.email.strip().lower()
    client_ip = get_client_ip(request)

    enforce_rate_limit(f"auth:login:ip:{client_ip}", limit=20, window_seconds=600)
    enforce_rate_limit(f"auth:login:email:{email}", limit=8, window_seconds=600)

    user = db.execute(select(User).where(User.email == email).limit(1)).scalar_one_or_none()

    if not user:
        audit_event(
            event_type="auth.login.failed",
            severity="warning",
            success=False,
            status_code=401,
            actor_type="anonymous",
            request=request,
            description="Login failed: unknown email",
            details={"email": email},
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        audit_event(
            event_type="auth.login.failed",
            severity="warning",
            success=False,
            status_code=401,
            actor_type="user",
            actor_user_id=user.id,
            target_user_id=user.id,
            request=request,
            description="Login failed: invalid password",
            details={"email": email},
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        audit_event(
            event_type="auth.login.blocked",
            severity="warning",
            success=False,
            status_code=403,
            actor_type="user",
            actor_user_id=user.id,
            target_user_id=user.id,
            request=request,
            description="Login blocked: inactive user",
            details={"email": email},
        )
        raise HTTPException(status_code=403, detail="Inactive user")

    if user.two_factor_enabled:
        enforce_rate_limit(f"auth:login:otp:{email}", limit=10, window_seconds=600)

        if not payload.otp_code:
            audit_event(
                event_type="auth.login.otp_required",
                severity="warning",
                success=False,
                status_code=401,
                actor_type="user",
                actor_user_id=user.id,
                target_user_id=user.id,
                request=request,
                description="Login blocked: OTP code required",
                details={"email": email},
            )
            raise HTTPException(status_code=401, detail="OTP code required")

        if not user.two_factor_secret:
            audit_event(
                event_type="auth.login.otp_misconfigured",
                severity="critical",
                success=False,
                status_code=500,
                actor_type="user",
                actor_user_id=user.id,
                target_user_id=user.id,
                request=request,
                description="Login blocked: 2FA enabled but secret missing",
                details={"email": email},
            )
            raise HTTPException(status_code=500, detail="2FA is enabled but secret is missing")

        totp = pyotp.TOTP(user.two_factor_secret)
        if not totp.verify(payload.otp_code, valid_window=1):
            audit_event(
                event_type="auth.login.failed_otp",
                severity="warning",
                success=False,
                status_code=401,
                actor_type="user",
                actor_user_id=user.id,
                target_user_id=user.id,
                request=request,
                description="Login failed: invalid OTP code",
                details={"email": email},
            )
            raise HTTPException(status_code=401, detail="Invalid OTP code")

    access_token = create_access_token(
        subject=str(user.id),
        extra={"is_admin": user.is_admin},
    )

    audit_event(
        event_type="auth.login.success",
        severity="info",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=user.id,
        target_user_id=user.id,
        request=request,
        description="Login successful",
        details={"email": user.email, "is_admin": user.is_admin},
    )

    return AuthTokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.get("/2fa/status", response_model=TwoFactorStatusResponse)
def two_factor_status(current_user: User = Depends(get_current_user)):
    return TwoFactorStatusResponse(enabled=current_user.two_factor_enabled)


@router.post("/2fa/setup", response_model=TwoFactorSetupResponse)
def setup_two_factor(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    client_ip = get_client_ip(request)

    enforce_rate_limit(f"auth:2fa:setup:ip:{client_ip}", limit=10, window_seconds=3600)
    enforce_rate_limit(f"auth:2fa:setup:user:{current_user.id}", limit=5, window_seconds=3600)

    if not current_user.two_factor_secret:
        current_user.two_factor_secret = pyotp.random_base32()
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    totp = pyotp.TOTP(current_user.two_factor_secret)
    otpauth_url = totp.provisioning_uri(name=current_user.email, issuer_name="SSD")

    audit_event(
        event_type="auth.2fa.setup",
        severity="info",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=current_user.id,
        target_user_id=current_user.id,
        request=request,
        description="2FA setup requested",
        details={"email": current_user.email, "already_enabled": current_user.two_factor_enabled},
    )

    return TwoFactorSetupResponse(
        secret=current_user.two_factor_secret,
        otpauth_url=otpauth_url,
        already_enabled=current_user.two_factor_enabled,
    )


@router.post("/2fa/confirm", response_model=TwoFactorStatusResponse)
def confirm_two_factor(
    payload: TwoFactorConfirmRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    client_ip = get_client_ip(request)

    enforce_rate_limit(f"auth:2fa:confirm:ip:{client_ip}", limit=20, window_seconds=600)
    enforce_rate_limit(f"auth:2fa:confirm:user:{current_user.id}", limit=8, window_seconds=600)

    if not current_user.two_factor_secret:
        audit_event(
            event_type="auth.2fa.confirm.failed",
            severity="warning",
            success=False,
            status_code=400,
            actor_type="user",
            actor_user_id=current_user.id,
            target_user_id=current_user.id,
            request=request,
            description="2FA confirm failed: setup not initialized",
        )
        raise HTTPException(status_code=400, detail="2FA setup not initialized")

    totp = pyotp.TOTP(current_user.two_factor_secret)
    if not totp.verify(payload.otp_code, valid_window=1):
        audit_event(
            event_type="auth.2fa.confirm.failed",
            severity="warning",
            success=False,
            status_code=400,
            actor_type="user",
            actor_user_id=current_user.id,
            target_user_id=current_user.id,
            request=request,
            description="2FA confirm failed: invalid OTP code",
        )
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    current_user.two_factor_enabled = True
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    audit_event(
        event_type="auth.2fa.confirm.success",
        severity="info",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=current_user.id,
        target_user_id=current_user.id,
        request=request,
        description="2FA enabled successfully",
    )

    return TwoFactorStatusResponse(enabled=current_user.two_factor_enabled)


@router.post("/2fa/disable", response_model=TwoFactorStatusResponse)
def disable_two_factor(
    payload: TwoFactorDisableRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    client_ip = get_client_ip(request)

    enforce_rate_limit(f"auth:2fa:disable:ip:{client_ip}", limit=10, window_seconds=600)
    enforce_rate_limit(f"auth:2fa:disable:user:{current_user.id}", limit=5, window_seconds=600)

    if not verify_password(payload.password, current_user.password_hash):
        audit_event(
            event_type="auth.2fa.disable.failed",
            severity="warning",
            success=False,
            status_code=401,
            actor_type="user",
            actor_user_id=current_user.id,
            target_user_id=current_user.id,
            request=request,
            description="2FA disable failed: invalid password",
        )
        raise HTTPException(status_code=401, detail="Invalid password")

    if current_user.two_factor_enabled:
        if not current_user.two_factor_secret:
            audit_event(
                event_type="auth.2fa.disable.failed",
                severity="critical",
                success=False,
                status_code=500,
                actor_type="user",
                actor_user_id=current_user.id,
                target_user_id=current_user.id,
                request=request,
                description="2FA disable failed: secret missing while enabled",
            )
            raise HTTPException(status_code=500, detail="2FA is enabled but secret is missing")

        totp = pyotp.TOTP(current_user.two_factor_secret)
        if not totp.verify(payload.otp_code, valid_window=1):
            audit_event(
                event_type="auth.2fa.disable.failed",
                severity="warning",
                success=False,
                status_code=401,
                actor_type="user",
                actor_user_id=current_user.id,
                target_user_id=current_user.id,
                request=request,
                description="2FA disable failed: invalid OTP code",
            )
            raise HTTPException(status_code=401, detail="Invalid OTP code")

    current_user.two_factor_enabled = False
    current_user.two_factor_secret = None
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    audit_event(
        event_type="auth.2fa.disable.success",
        severity="warning",
        success=True,
        status_code=200,
        actor_type="user",
        actor_user_id=current_user.id,
        target_user_id=current_user.id,
        request=request,
        description="2FA disabled",
    )

    return TwoFactorStatusResponse(enabled=current_user.two_factor_enabled)