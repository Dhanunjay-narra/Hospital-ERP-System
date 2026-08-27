from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.billing.schemas import (
    InvoiceCreate, InvoiceResponse,
    PaymentTransactionCreate, PaymentTransactionResponse
)
from app.modules.billing.service import BillingService

router = APIRouter(prefix="/billing", tags=["Billing & Finance"])

@router.get("/invoices", response_model=PaginatedResponse[InvoiceResponse])
def list_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    invoices, total = BillingService.get_invoices(db, skip=params.skip, limit=params.limit, patient_id=patient_id, status=status)
    return PaginatedResponse.create(items=invoices, total=total, params=params)

@router.post("/invoices", response_model=InvoiceResponse)
def create_invoice(
    inv_in: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "ACCOUNTANT"))
):
    return BillingService.create_invoice(db, inv_in, created_by=current_user.id)

@router.post("/payments", response_model=PaymentTransactionResponse)
def record_payment(
    pay_in: PaymentTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "ACCOUNTANT"))
):
    return BillingService.record_payment(db, pay_in, cashier_id=current_user.id)
