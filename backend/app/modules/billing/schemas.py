from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class InvoiceItemCreate(BaseModel):
    service_name: str
    service_code: Optional[str] = None
    quantity: int = 1
    unit_price: float
    discount_percent: float = 0.0
    tax_amount: float = 0.0

class InvoiceItemResponse(InvoiceItemCreate):
    id: str
    total_price: float

    class Config:
        from_attributes = True

class PaymentTransactionCreate(BaseModel):
    invoice_id: str
    amount: float
    payment_method: str = "CASH" # CASH, CREDIT_CARD, UPI, INSURANCE_CLAIM
    transaction_reference: Optional[str] = None
    notes: Optional[str] = None

class PaymentTransactionResponse(PaymentTransactionCreate):
    id: str
    receipt_number: str
    patient_id: str
    payment_date: datetime

    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    patient_id: str
    admission_id: Optional[str] = None
    opd_visit_id: Optional[str] = None
    items: List[InvoiceItemCreate]

class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    subtotal: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance_amount: float
    status: str
    invoice_date: datetime
    patient: Optional[PatientResponse] = None
    items: List[InvoiceItemResponse] = []
    payments: List[PaymentTransactionResponse] = []

    class Config:
        from_attributes = True
