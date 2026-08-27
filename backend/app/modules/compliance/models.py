import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class DataPrivacyConsent(BaseModel):
    __tablename__ = "data_privacy_consents"

    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    # Mandates: HIPAA, GDPR, ABDM_AYUSHMAN_BHARAT
    compliance_framework = Column(String(50), default="HIPAA", nullable=False)
    purpose_of_processing = Column(String(200), default="Direct Clinical Care & Electronic Billing", nullable=False)
    is_consent_granted = Column(Boolean, default=True, nullable=False)
    consent_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    revocation_timestamp = Column(DateTime, nullable=True)

    patient = relationship("Patient", lazy="joined")

class SecurityEventLog(BaseModel):
    __tablename__ = "security_event_logs"

    event_type = Column(String(100), nullable=False) # FAILED_LOGIN_ATTEMPT, UNAUTHORIZED_MRD_ACCESS, ROLE_ESCALATION, PHI_EXPORT
    severity = Column(String(30), default="MEDIUM", nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    actor_user_id = Column(String(36), nullable=True)
    ip_address = Column(String(50), default="127.0.0.1", nullable=False)
    user_agent = Column(String(255), nullable=True)
    details = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
