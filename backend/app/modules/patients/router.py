from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.patients.schemas import PatientCreate, PatientUpdate, PatientResponse, Patient360Summary
from app.modules.patients.service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients Master"])

@router.get("", response_model=PaginatedResponse[PatientResponse])
def list_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    patients, total = PatientService.get_all(db, skip=params.skip, limit=params.limit, search=search)
    return PaginatedResponse.create(items=patients, total=total, params=params)

@router.post("", response_model=PatientResponse)
def register_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PatientService.create(db, patient_in, created_by=current_user.id)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = PatientService.get_by_id(db, patient_id)
    if not patient:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Patient not found")
    return patient

@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: str,
    patient_in: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PatientService.update(db, patient_id, patient_in, updated_by=current_user.id)

@router.get("/{patient_id}/360", response_model=Patient360Summary)
def get_patient_360(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PatientService.get_patient_360(db, patient_id)
