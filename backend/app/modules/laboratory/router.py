from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.laboratory.schemas import (
    LabTestCatalogCreate, LabTestCatalogResponse,
    LabOrderCreate, LabOrderResponse,
    LabResultResponse
)
from app.modules.laboratory.service import LabService

router = APIRouter(prefix="/laboratory", tags=["Laboratory & Pathology"])

@router.get("/catalog", response_model=List[LabTestCatalogResponse])
def get_lab_catalog(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return LabService.get_catalog(db)

@router.post("/catalog", response_model=LabTestCatalogResponse)
def create_lab_test(
    test_in: LabTestCatalogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "LAB_TECHNICIAN"))
):
    return LabService.create_test(db, test_in)

@router.get("/orders", response_model=PaginatedResponse[LabOrderResponse])
def list_lab_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    orders, total = LabService.get_orders(db, skip=params.skip, limit=params.limit, patient_id=patient_id, status=status)
    return PaginatedResponse.create(items=orders, total=total, params=params)

@router.post("/orders", response_model=LabOrderResponse)
def create_lab_order(
    order_in: LabOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return LabService.create_order(db, order_in, created_by=current_user.id)

@router.post("/results/{result_id}", response_model=LabResultResponse)
def enter_lab_result(
    result_id: str,
    value: str,
    numeric_value: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "LAB_TECHNICIAN"))
):
    return LabService.enter_result(db, result_id, value, numeric_value)
