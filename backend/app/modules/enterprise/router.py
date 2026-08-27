from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.enterprise.schemas import BranchTransferCreate, BranchTransferResponse
from app.modules.enterprise.service import EnterpriseService

router = APIRouter(prefix="/enterprise", tags=["Multi-Branch & Enterprise Rollup"])

@router.get("/transfers", response_model=PaginatedResponse[BranchTransferResponse])
def list_branch_transfers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    transfers, total = EnterpriseService.get_transfers(db, skip=params.skip, limit=params.limit)
    return PaginatedResponse.create(items=transfers, total=total, params=params)

@router.post("/transfers", response_model=BranchTransferResponse)
def request_branch_transfer(
    tr_in: BranchTransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return EnterpriseService.create_transfer(db, tr_in, created_by=current_user.id)
