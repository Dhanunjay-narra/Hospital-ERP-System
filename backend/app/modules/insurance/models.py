import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class InsuranceProvider(BaseModel):
    __tablename__ = "insurance_providers"

    name = Column(String(200), unique=True, index=True, nullable=False) # BlueCross BlueShield, Aetna, Cigna, Medicare
    code = Column(String(50), unique=True, nullable=False) # BCBS, AETNA, CIGNA
    tpa_name = Column(String(200), nullable=True) # Third Party Administrator Name
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    portal_url = Column(String(255), nullable=True)
    claim_submission_format = Column(String(50), default="ELECTRONIC_EDI_837", nullable=False)

class InsuranceClaim(BaseModel):
    __tablename__ = "insurance_claims"

    claim_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. CLM-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(String(36), ForeignKey("insurance_providers.id", ondelete="CASCADE"), nullable=False)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)

    policy_number = Column(String(100), nullable=False)
    pre_auth_number = Column(String(100), nullable=True)
    
    total_claim_amount = Column(Float, default=0.0, nullable=False)
    approved_amount = Column(Float, default=0.0, nullable=False)
    patient_copay_amount = Column(Float, default=0.0, nullable=False)
    deduction_amount = Column(Float, default=0.0, nullable=False)
    
    # STATUS: DRAFT, PRE_AUTH_REQUESTED, PRE_AUTH_APPROVED, SUBMITTED, QUERY_RAISED, APPROVED, SETTLED, REJECTED
    status = Column(String(50), default="SUBMITTED", index=True, nullable=False)
    rejection_reason = Column(Text, nullable=True)
    submission_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    settlement_date = Column(DateTime, nullable=True)

    patient = relationship("Patient", lazy="joined")
    provider = relationship("InsuranceProvider", lazy="joined")
    invoice = relationship("Invoice", lazy="joined")
