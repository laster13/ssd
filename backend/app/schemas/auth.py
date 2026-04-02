from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, StringConstraints

PasswordStr = Annotated[str, StringConstraints(min_length=14, max_length=128)]
OtpStr = Annotated[str, StringConstraints(pattern=r"^\d{6}$")]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    otp_code: OtpStr | None = None


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class TwoFactorSetupResponse(BaseModel):
    secret: str
    otpauth_url: str
    already_enabled: bool


class TwoFactorConfirmRequest(BaseModel):
    otp_code: OtpStr


class TwoFactorDisableRequest(BaseModel):
    password: PasswordStr
    otp_code: OtpStr


class TwoFactorStatusResponse(BaseModel):
    enabled: bool