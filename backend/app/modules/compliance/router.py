from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.compliance.schemas import (
    DataPrivacyConsentCreate, DataPrivacyConsentResponse,
    SecurityEventLogCreate, SecurityEventLogResponse
)
from app.modules.compliance.service import ComplianceService

router = APIRouter(prefix="/compliance", tags=["Security, Privacy & Compliance"])

@router.get("/privacy-consents", response_model=List[DataPrivacyConsentResponse])
def list_privacy_consents(
    patient_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ComplianceService.get_privacy_consents(db, patient_id=patient_id)

@router.post("/privacy-consents", response_model=DataPrivacyConsentResponse)
def record_privacy_consent(
    con_in: DataPrivacyConsentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ComplianceService.record_privacy_consent(db, con_in)

@router.get("/security-events", response_model=PaginatedResponse[SecurityEventLogResponse])
def list_security_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "COMPLIANCE_OFFICER"))
):
    params = PaginationParams(page=page, page_size=page_size)
    events, total = ComplianceService.get_security_events(db, skip=params.skip, limit=params.limit)
    return PaginatedResponse.create(items=events, total=total, params=params)

@router.post("/security-events", response_model=SecurityEventLogResponse)
def log_security_event(
    ev_in: SecurityEventLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ComplianceService.log_security_event(db, ev_in, actor_user_id=current_user.id)
