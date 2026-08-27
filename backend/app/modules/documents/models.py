import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class PatientDocument(BaseModel):
    __tablename__ = "patient_documents"

    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    
    document_title = Column(String(200), nullable=False) # General Informed Consent, Surgery Consent, Insurance Card Copy
    # Category: CONSENT_FORM, IDENTITY_PROOF, INSURANCE_CARD, DISCHARGE_SUMMARY, EXTERNAL_REPORT
    category = Column(String(50), default="CONSENT_FORM", nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size_kb = Column(Integer, default=150, nullable=False)
    mime_type = Column(String(100), default="application/pdf", nullable=False)
    
    # Digital Signature
    is_digitally_signed = Column(Boolean, default=True, nullable=False)
    signed_by_name = Column(String(150), nullable=True)
    signed_at = Column(DateTime, default=datetime.utcnow, nullable=True)

    patient = relationship("Patient", lazy="joined")
