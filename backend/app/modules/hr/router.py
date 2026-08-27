from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.hr.schemas import (
    EmployeeCreate, EmployeeResponse,
    StaffLeaveCreate, StaffLeaveResponse
)
from app.modules.hr.service import HRService

router = APIRouter(prefix="/hr", tags=["Staff & HR Management"])

@router.get("/employees", response_model=PaginatedResponse[EmployeeResponse])
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    department_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    employees, total = HRService.get_employees(db, skip=params.skip, limit=params.limit, department_id=department_id)
    return PaginatedResponse.create(items=employees, total=total, params=params)

@router.post("/employees", response_model=EmployeeResponse)
def create_employee(
    emp_in: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "HR_MANAGER"))
):
    return HRService.create_employee(db, emp_in, created_by=current_user.id)

@router.get("/leaves", response_model=List[StaffLeaveResponse])
def list_leaves(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return HRService.get_leaves(db)

@router.post("/leaves", response_model=StaffLeaveResponse)
def apply_leave(
    leave_in: StaffLeaveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return HRService.request_leave(db, leave_in, created_by=current_user.id)
