from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class PermissionBase(BaseModel):
    name: str
    code: str
    module: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: Optional[List[str]] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[str]] = None

class RoleResponse(RoleBase):
    id: str
    is_system: bool
    created_at: datetime
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    branch_id: Optional[str] = None
    department_id: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role_ids: Optional[List[str]] = []

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    branch_id: Optional[str] = None
    department_id: Optional[str] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[str]] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    is_mfa_enabled: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True
