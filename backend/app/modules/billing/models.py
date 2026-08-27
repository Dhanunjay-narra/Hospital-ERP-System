import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ServiceChargeMaster(BaseModel):
    __tablename__ = "service_charge_master"

    service_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. CHG-CONSULT-GEN, CHG-BED-ICU, CHG-LAB-CBC
    service_name = Column(String(200), nullable=False)
    category = Column(String(100), default="CONSULTATION", nullable=False) # CONSULTATION, BED_CHARGE, PROCEDURE, LAB, RADIOLOGY, PHARMACY, OT
    standard_rate = Column(Float, default=0.0, nullable=False)
    tax_percentage = Column(Float, default=0.0, nullable=False) # 0%, 5%, 18%
    is_discountable = Column(Boolean, default=True, nullable=False)

class Invoice(BaseModel):
    __tablename__ = "invoices"

    invoice_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. INV-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    opd_visit_id = Column(String(36), ForeignKey("opd_visits.id", ondelete="SET NULL"), nullable=True)
    
    subtotal = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    paid_amount = Column(Float, default=0.0, nullable=False)
    balance_amount = Column(Float, default=0.0, nullable=False)
    
    # STATUS: DRAFT, ISSUED, PARTIALLY_PAID, PAID, VOIDED, REFUNDED
    status = Column(String(50), default="ISSUED", index=True, nullable=False)
    due_date = Column(DateTime, nullable=True)
    invoice_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("Patient", lazy="joined")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan", lazy="joined")
    payments = relationship("PaymentTransaction", back_populates="invoice", cascade="all, delete-orphan", lazy="joined")

class InvoiceItem(BaseModel):
    __tablename__ = "invoice_items"

    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    service_name = Column(String(200), nullable=False)
    service_code = Column(String(50), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, default=0.0, nullable=False)
    discount_percent = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total_price = Column(Float, default=0.0, nullable=False)

    invoice = relationship("Invoice", back_populates="items")

class PaymentTransaction(BaseModel):
    __tablename__ = "payment_transactions"

    receipt_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. REC-2026-0001
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    
    amount = Column(Float, nullable=False)
    # Payment method: CASH, CREDIT_CARD, DEBIT_CARD, UPI, BANK_TRANSFER, INSURANCE_CLAIM
    payment_method = Column(String(50), default="CASH", nullable=False)
    transaction_reference = Column(String(100), nullable=True) # Gateway Txn ID / Check #
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    cashier_id = Column(String(36), nullable=True)
    notes = Column(Text, nullable=True)

    invoice = relationship("Invoice", back_populates="payments")
    patient = relationship("Patient", lazy="joined")
