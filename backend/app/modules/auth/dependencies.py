from typing import List, Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.modules.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    actual_token = token
    if not actual_token and authorization and authorization.startswith("Bearer "):
        actual_token = authorization.split(" ")[1]

    if not actual_token:
        raise UnauthorizedError("Missing authentication credentials")

    payload = decode_token(actual_token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedError("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise UnauthorizedError("User not found or inactive")

    return user

def require_permissions(*required_permissions: str):
    """Dependency factory for checking user permissions"""
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        user_roles = [r.code for r in current_user.roles]
        if "SUPER_ADMIN" in user_roles or "HOSPITAL_ADMIN" in user_roles:
            return current_user

        user_perms = set()
        for role in current_user.roles:
            for perm in role.permissions:
                user_perms.add(perm.code)

        for req in required_permissions:
            if req not in user_perms:
                raise ForbiddenError(f"Missing required permission: {req}")

        return current_user
    return permission_checker

def require_roles(*required_roles: str):
    """Dependency factory for checking user roles"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_roles = [r.code for r in current_user.roles]
        if "SUPER_ADMIN" in user_roles:
            return current_user

        for req_role in required_roles:
            if req_role in user_roles:
                return current_user

        raise ForbiddenError(f"User requires one of the following roles: {', '.join(required_roles)}")
    return role_checker
