from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.opd.schemas import (
    OPDVisitCreate, OPDConsultationUpdate, OPDVisitResponse,
    VitalSignsCreate, VitalSignsResponse
)
from app.modules.opd.service import OPDService

router = APIRouter(prefix="/opd", tags=["OPD Management"])

@router.get("/visits", response_model=PaginatedResponse[OPDVisitResponse])
def list_opd_visits(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    doctor_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    visits, total = OPDService.get_all_visits(db, skip=params.skip, limit=params.limit, doctor_id=doctor_id, status=status)
    return PaginatedResponse.create(items=visits, total=total, params=params)

@router.post("/visits", response_model=OPDVisitResponse)
def create_opd_visit(
    visit_in: OPDVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OPDService.create_visit(db, visit_in, created_by=current_user.id)

@router.patch("/visits/{visit_id}/consultation", response_model=OPDVisitResponse)
def complete_consultation(
    visit_id: str,
    consult_in: OPDConsultationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OPDService.record_consultation(db, visit_id, consult_in)

@router.post("/vitals", response_model=VitalSignsResponse)
def record_patient_vitals(
    vitals_in: VitalSignsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OPDService.record_vitals(db, vitals_in, recorded_by=current_user.id)
