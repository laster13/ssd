from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
import pyotp

from app.api.deps import get_current_user
from app.core.auth import create_access_token, hash_password, verify_password
from app.core.database import get_db
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
    db: Session = Depends(get_db),
):
    existing = db.execute(select(User).where(User.email == payload.email).limit(1)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    is_first_user = db.execute(select(User)).scalars().first() is None

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,
        is_admin=is_first_user,
        two_factor_enabled=False,
        two_factor_secret=None,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

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
    db: Session = Depends(get_db),
):
    user = db.execute(select(User).where(User.email == payload.email).limit(1)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    if user.two_factor_enabled:
        if not payload.otp_code:
            raise HTTPException(status_code=401, detail="OTP code required")

        if not user.two_factor_secret:
            raise HTTPException(status_code=500, detail="2FA is enabled but secret is missing")

        totp = pyotp.TOTP(user.two_factor_secret)
        if not totp.verify(payload.otp_code, valid_window=1):
            raise HTTPException(status_code=401, detail="Invalid OTP code")

    access_token = create_access_token(
        subject=str(user.id),
        extra={"is_admin": user.is_admin},
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.two_factor_secret:
        current_user.two_factor_secret = pyotp.random_base32()
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    totp = pyotp.TOTP(current_user.two_factor_secret)
    otpauth_url = totp.provisioning_uri(
        name=current_user.email,
        issuer_name="SSD"
    )

    return TwoFactorSetupResponse(
        secret=current_user.two_factor_secret,
        otpauth_url=otpauth_url,
        already_enabled=current_user.two_factor_enabled,
    )


@router.post("/2fa/confirm", response_model=TwoFactorStatusResponse)
def confirm_two_factor(
    payload: TwoFactorConfirmRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.two_factor_secret:
        raise HTTPException(status_code=400, detail="2FA setup not initialized")

    totp = pyotp.TOTP(current_user.two_factor_secret)
    if not totp.verify(payload.otp_code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    current_user.two_factor_enabled = True
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return TwoFactorStatusResponse(enabled=current_user.two_factor_enabled)


@router.post("/2fa/disable", response_model=TwoFactorStatusResponse)
def disable_two_factor(
    payload: TwoFactorDisableRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.password, current_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    if current_user.two_factor_enabled:
        if not current_user.two_factor_secret:
            raise HTTPException(status_code=500, detail="2FA is enabled but secret is missing")

        totp = pyotp.TOTP(current_user.two_factor_secret)
        if not totp.verify(payload.otp_code, valid_window=1):
            raise HTTPException(status_code=401, detail="Invalid OTP code")

    current_user.two_factor_enabled = False
    current_user.two_factor_secret = None
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return TwoFactorStatusResponse(enabled=current_user.two_factor_enabled)