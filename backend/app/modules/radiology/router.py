from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.radiology.schemas import (
    RadiologyOrderCreate, RadiologyReportSubmit, RadiologyOrderResponse
)
from app.modules.radiology.service import RadiologyService

router = APIRouter(prefix="/radiology", tags=["Radiology & Imaging"])

@router.get("/orders", response_model=PaginatedResponse[RadiologyOrderResponse])
def list_radiology_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    modality: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    orders, total = RadiologyService.get_orders(db, skip=params.skip, limit=params.limit, modality=modality, status=status)
    return PaginatedResponse.create(items=orders, total=total, params=params)

@router.post("/orders", response_model=RadiologyOrderResponse)
def create_radiology_order(
    order_in: RadiologyOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RadiologyService.create_order(db, order_in, created_by=current_user.id)

@router.post("/orders/{order_id}/report", response_model=RadiologyOrderResponse)
def submit_radiology_report(
    order_id: str,
    report_in: RadiologyReportSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "RADIOLOGIST"))
):
    return RadiologyService.submit_report(db, order_id, report_in, radiologist_id=current_user.id)
