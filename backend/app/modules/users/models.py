import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, Integer, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.database import Base

# Association table for User <-> Role
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)

# Association table for Role <-> Permission
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", String(36), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(30), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Status & Flags
    is_verified = Column(Boolean, default=False, nullable=False)
    is_mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(100), nullable=True)
    must_change_password = Column(Boolean, default=False, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    
    # Organization mapping
    branch_id = Column(String(36), ForeignKey("hospital_branches.id", ondelete="SET NULL"), nullable=True)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users", lazy="joined")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles", lazy="joined")

class Permission(BaseModel):
    __tablename__ = "permissions"

    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)
    module = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=True)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class UserSession(BaseModel):
    __tablename__ = "user_sessions"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    refresh_token = Column(String(500), index=True, nullable=False)
    user_agent = Column(String(300), nullable=True)
    ip_address = Column(String(50), nullable=True)
    device_info = Column(String(200), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="sessions")

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    actor_id = Column(String(36), nullable=True, index=True)
    actor_email = Column(String(255), nullable=True)
    action = Column(String(100), nullable=False, index=True)  # e.g., CREATE, UPDATE, DELETE, LOGIN
    resource_type = Column(String(100), nullable=False, index=True)  # e.g., Patient, Bill, Prescription
    resource_id = Column(String(36), nullable=True, index=True)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(300), nullable=True)
    status = Column(String(20), default="SUCCESS", nullable=False)  # SUCCESS, FAILED
