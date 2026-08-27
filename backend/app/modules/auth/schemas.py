from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.modules.users.schemas import UserResponse

class LoginRequest(BaseModel):
    username_or_email: str
    password: str
    mfa_code: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class MFAEnableResponse(BaseModel):
    secret: str
    otpauth_url: str
    qr_code_base64: str

class MFAVerifyRequest(BaseModel):
    code: str
