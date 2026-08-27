from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.modules.users.models import User, UserSession
from app.modules.users.service import UserService
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.core.config import settings

class AuthService:
    @staticmethod
    def authenticate(db: Session, login_data: LoginRequest, user_agent: Optional[str] = None, ip_address: Optional[str] = None) -> TokenResponse:
        user = db.query(User).filter(
            (User.email == login_data.username_or_email) | (User.username == login_data.username_or_email)
        ).first()

        if not user or not verify_password(login_data.password, user.hashed_password):
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=15)
                db.commit()
            raise UnauthorizedError("Invalid username/email or password")

        if not user.is_active:
            raise ForbiddenError("User account is deactivated")

        if user.locked_until and user.locked_until > datetime.utcnow():
            raise ForbiddenError(f"Account temporarily locked until {user.locked_until.isoformat()}")

        user.failed_login_attempts = 0
        user.last_login_at = datetime.utcnow()

        roles = [r.code for r in user.roles]
        claims = {
            "email": user.email,
            "username": user.username,
            "roles": roles,
            "tenant_id": user.tenant_id
        }

        access_token = create_access_token(subject=user.id, extra_claims=claims)
        refresh_token = create_refresh_token(subject=user.id)

        session = UserSession(
            user_id=user.id,
            refresh_token=refresh_token,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(session)
        db.commit()
        db.refresh(user)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user
        )

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")

        user_id = payload.get("sub")
        session = db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token,
            UserSession.is_revoked == False,
            UserSession.expires_at > datetime.utcnow()
        ).first()

        if not session:
            raise UnauthorizedError("Session expired or revoked")

        user = UserService.get_by_id(db, user_id)
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")

        roles = [r.code for r in user.roles]
        claims = {
            "email": user.email,
            "username": user.username,
            "roles": roles,
            "tenant_id": user.tenant_id
        }

        new_access_token = create_access_token(subject=user.id, extra_claims=claims)
        new_refresh_token = create_refresh_token(subject=user.id)

        session.refresh_token = new_refresh_token
        session.expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        db.commit()

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user
        )
