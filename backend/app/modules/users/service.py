from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.users.models import User, Role, Permission
from app.modules.users.schemas import UserCreate, UserUpdate, RoleCreate, RoleUpdate
from app.core.security import get_password_hash
from app.core.exceptions import NotFoundError, ConflictError

class UserService:
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> (List[User], int):
        query = db.query(User)
        if search:
            query = query.filter(
                (User.first_name.ilike(f"%{search}%")) |
                (User.last_name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%")) |
                (User.username.ilike(f"%{search}%"))
            )
        total = query.count()
        users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
        return users, total

    @staticmethod
    def create(db: Session, user_in: UserCreate, created_by: Optional[str] = None) -> User:
        if UserService.get_by_email(db, user_in.email):
            raise ConflictError("User with this email already exists")
        if UserService.get_by_username(db, user_in.username):
            raise ConflictError("User with this username already exists")

        user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            phone_number=user_in.phone_number,
            branch_id=user_in.branch_id,
            department_id=user_in.department_id,
            created_by=created_by
        )

        if user_in.role_ids:
            roles = db.query(Role).filter(Role.id.in_(user_in.role_ids)).all()
            user.roles = roles

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db: Session, user_id: str, user_in: UserUpdate, updated_by: Optional[str] = None) -> User:
        user = UserService.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")

        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            user.hashed_password = get_password_hash(update_data.pop("password"))

        if "role_ids" in update_data:
            role_ids = update_data.pop("role_ids")
            if role_ids is not None:
                user.roles = db.query(Role).filter(Role.id.in_(role_ids)).all()

        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_by = updated_by
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: str) -> bool:
        user = UserService.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        user.is_active = False
        db.commit()
        return True

class RoleService:
    @staticmethod
    def get_all(db: Session) -> List[Role]:
        return db.query(Role).all()

    @staticmethod
    def get_by_id(db: Session, role_id: str) -> Optional[Role]:
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def create(db: Session, role_in: RoleCreate) -> Role:
        existing = db.query(Role).filter((Role.name == role_in.name) | (Role.code == role_in.code)).first()
        if existing:
            raise ConflictError("Role with this name or code already exists")

        role = Role(name=role_in.name, code=role_in.code, description=role_in.description)
        if role_in.permission_ids:
            perms = db.query(Permission).filter(Permission.id.in_(role_in.permission_ids)).all()
            role.permissions = perms

        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def get_all_permissions(db: Session) -> List[Permission]:
        return db.query(Permission).all()
