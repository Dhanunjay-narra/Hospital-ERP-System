from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.ipd.schemas import (
    AdmissionCreate, DischargeRequest, AdmissionResponse,
    DailyClinicalRoundCreate, DailyClinicalRoundResponse
)
from app.modules.ipd.service import IPDService

router = APIRouter(prefix="/ipd", tags=["IPD & Admission Management"])

@router.get("/admissions", response_model=PaginatedResponse[AdmissionResponse])
def list_admissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    ward_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    admissions, total = IPDService.get_all_admissions(
        db,
        skip=params.skip,
        limit=params.limit,
        ward_id=ward_id,
        doctor_id=doctor_id,
        status=status
    )
    return PaginatedResponse.create(items=admissions, total=total, params=params)

@router.post("/admissions", response_model=AdmissionResponse)
def admit_patient(
    adm_in: AdmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return IPDService.admit_patient(db, adm_in, created_by=current_user.id)

@router.get("/admissions/{admission_id}", response_model=AdmissionResponse)
def get_admission(
    admission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    adm = IPDService.get_admission_by_id(db, admission_id)
    if not adm:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Admission not found")
    return adm

@router.post("/admissions/{admission_id}/discharge", response_model=AdmissionResponse)
def discharge_patient(
    admission_id: str,
    dis_in: DischargeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "DOCTOR"))
):
    return IPDService.discharge_patient(db, admission_id, dis_in)

@router.post("/daily-rounds", response_model=DailyClinicalRoundResponse)
def add_daily_round(
    round_in: DailyClinicalRoundCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "DOCTOR"))
):
    return IPDService.add_daily_round(db, round_in, doctor_id=round_in.doctor_id)
