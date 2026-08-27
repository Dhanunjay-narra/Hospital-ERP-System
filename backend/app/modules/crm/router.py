from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.crm.schemas import (
    PatientLeadCreate, PatientLeadResponse,
    LeadInteractionCreate, LeadInteractionResponse
)
from app.modules.crm.service import CRMService

router = APIRouter(prefix="/crm", tags=["Patient CRM & Leads"])

@router.get("/leads", response_model=PaginatedResponse[PatientLeadResponse])
def list_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    leads, total = CRMService.get_leads(db, skip=params.skip, limit=params.limit, status=status)
    return PaginatedResponse.create(items=leads, total=total, params=params)

@router.post("/leads", response_model=PatientLeadResponse)
def create_lead(
    lead_in: PatientLeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CRMService.create_lead(db, lead_in, created_by=current_user.id)

@router.post("/leads/{lead_id}/interactions", response_model=LeadInteractionResponse)
def log_lead_interaction(
    lead_id: str,
    inter_in: LeadInteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CRMService.add_interaction(db, lead_id, inter_in, user_id=current_user.id)
