from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.insurance.schemas import (
    InsuranceProviderCreate, InsuranceProviderResponse,
    InsuranceClaimCreate, InsuranceClaimResponse
)
from app.modules.insurance.service import InsuranceService

router = APIRouter(prefix="/insurance", tags=["Insurance & TPA Claims"])

@router.get("/providers", response_model=List[InsuranceProviderResponse])
def list_providers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InsuranceService.get_providers(db)

@router.post("/providers", response_model=InsuranceProviderResponse)
def create_provider(
    prov_in: InsuranceProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "ACCOUNTANT"))
):
    return InsuranceService.create_provider(db, prov_in)

@router.get("/claims", response_model=PaginatedResponse[InsuranceClaimResponse])
def list_claims(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    claims, total = InsuranceService.get_claims(db, skip=params.skip, limit=params.limit, patient_id=patient_id, status=status)
    return PaginatedResponse.create(items=claims, total=total, params=params)

@router.post("/claims", response_model=InsuranceClaimResponse)
def submit_claim(
    claim_in: InsuranceClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "ACCOUNTANT"))
):
    return InsuranceService.submit_claim(db, claim_in, created_by=current_user.id)
