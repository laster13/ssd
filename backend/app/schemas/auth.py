from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    otp_code: str | None = None


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
    otp_code: str


class TwoFactorDisableRequest(BaseModel):
    password: str
    otp_code: str


class TwoFactorStatusResponse(BaseModel):
    enabled: bool