from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.doctors.schemas import DoctorCreate, DoctorUpdate, DoctorResponse
from app.modules.doctors.service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors & Providers"])

@router.get("", response_model=PaginatedResponse[DoctorResponse])
def list_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    specialization: Optional[str] = None,
    department_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    doctors, total = DoctorService.get_all(db, skip=params.skip, limit=params.limit, specialization=specialization, department_id=department_id)
    return PaginatedResponse.create(items=doctors, total=total, params=params)

@router.post("", response_model=DoctorResponse)
def create_doctor(
    doc_in: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "HR_MANAGER"))
):
    return DoctorService.create(db, doc_in, created_by=current_user.id)

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = DoctorService.get_by_id(db, doctor_id)
    if not doc:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Doctor not found")
    return doc

@router.patch("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: str,
    doc_in: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "DOCTOR"))
):
    return DoctorService.update(db, doctor_id, doc_in)
