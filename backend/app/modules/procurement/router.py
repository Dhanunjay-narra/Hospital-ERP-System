from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.procurement.schemas import (
    VendorCreate, VendorResponse,
    PurchaseOrderCreate, PurchaseOrderResponse
)
from app.modules.procurement.service import ProcurementService

router = APIRouter(prefix="/procurement", tags=["Procurement & Vendors"])

@router.get("/vendors", response_model=List[VendorResponse])
def list_vendors(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ProcurementService.get_vendors(db)

@router.post("/vendors", response_model=VendorResponse)
def create_vendor(
    ven_in: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "PROCUREMENT_OFFICER"))
):
    return ProcurementService.create_vendor(db, ven_in)

@router.get("/purchase-orders", response_model=PaginatedResponse[PurchaseOrderResponse])
def list_purchase_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    vendor_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    pos, total = ProcurementService.get_purchase_orders(db, skip=params.skip, limit=params.limit, vendor_id=vendor_id, status=status)
    return PaginatedResponse.create(items=pos, total=total, params=params)

@router.post("/purchase-orders", response_model=PurchaseOrderResponse)
def create_purchase_order(
    po_in: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "PROCUREMENT_OFFICER"))
):
    return ProcurementService.create_purchase_order(db, po_in, created_by=current_user.id)
