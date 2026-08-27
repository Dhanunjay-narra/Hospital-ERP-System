from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.emergency.schemas import EmergencyTriageCreate, EmergencyTriageResponse
from app.modules.emergency.service import EmergencyService

router = APIRouter(prefix="/emergency", tags=["Emergency & Trauma"])

@router.get("/triage", response_model=PaginatedResponse[EmergencyTriageResponse])
def list_triages(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    priority: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    triages, total = EmergencyService.get_all_triages(db, skip=params.skip, limit=params.limit, priority=priority, status=status)
    return PaginatedResponse.create(items=triages, total=total, params=params)

@router.post("/triage", response_model=EmergencyTriageResponse)
def register_triage(
    triage_in: EmergencyTriageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return EmergencyService.create_triage(db, triage_in, created_by=current_user.id)
