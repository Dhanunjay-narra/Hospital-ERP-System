from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_permissions, require_roles
from app.modules.users.models import User
from app.modules.users.schemas import (
    UserCreate, UserUpdate, UserResponse,
    RoleCreate, RoleUpdate, RoleResponse,
    PermissionResponse
)
from app.modules.users.service import UserService, RoleService

router = APIRouter(prefix="/users", tags=["Users & RBAC"])

@router.get("", response_model=PaginatedResponse[UserResponse])
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    users, total = UserService.get_all(db, skip=params.skip, limit=params.limit, search=search)
    return PaginatedResponse.create(items=users, total=total, params=params)

@router.post("", response_model=UserResponse)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return UserService.create(db, user_in, created_by=current_user.id)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = UserService.get_by_id(db, user_id)
    if not user:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("User not found")
    return user

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return UserService.update(db, user_id, user_in, updated_by=current_user.id)

@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    UserService.delete(db, user_id)
    return {"message": "User deactivated successfully"}

# Roles and Permissions endpoints
roles_router = APIRouter(prefix="/roles", tags=["Roles & Permissions"])

@roles_router.get("", response_model=List[RoleResponse])
def list_roles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return RoleService.get_all(db)

@roles_router.post("", response_model=RoleResponse)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return RoleService.create(db, role_in)

@roles_router.get("/permissions", response_model=List[PermissionResponse])
def list_permissions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return RoleService.get_all_permissions(db)
