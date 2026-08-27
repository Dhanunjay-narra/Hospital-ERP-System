from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.schemas import LoginRequest, TokenResponse, RefreshTokenRequest, PasswordChangeRequest
from app.modules.auth.service import AuthService
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.users.schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user_agent = request.headers.get("user-agent")
    client_ip = request.client.host if request.client else None
    return AuthService.authenticate(db, login_data, user_agent=user_agent, ip_address=client_ip)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return AuthService.refresh_access_token(db, payload.refresh_token)

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}
