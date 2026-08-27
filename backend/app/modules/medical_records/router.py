from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.medical_records.schemas import (
    MedicalRecordArchiveCreate, MedicalRecordArchiveResponse,
    RecordAccessLogCreate, RecordAccessLogResponse
)
from app.modules.medical_records.service import MedicalRecordService

router = APIRouter(prefix="/medical-records", tags=["Medical Records (MRD)"])

@router.get("/archives", response_model=PaginatedResponse[MedicalRecordArchiveResponse])
def list_archives(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    arcs, total = MedicalRecordService.get_archives(db, skip=params.skip, limit=params.limit, patient_id=patient_id)
    return PaginatedResponse.create(items=arcs, total=total, params=params)

@router.post("/archives", response_model=MedicalRecordArchiveResponse)
def archive_patient_record(
    arc_in: MedicalRecordArchiveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "MRD_OFFICER"))
):
    return MedicalRecordService.archive_record(db, arc_in, created_by=current_user.id)

@router.post("/access-logs", response_model=RecordAccessLogResponse)
def log_record_access(
    log_in: RecordAccessLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return MedicalRecordService.log_access(db, log_in, user_id=current_user.id)
