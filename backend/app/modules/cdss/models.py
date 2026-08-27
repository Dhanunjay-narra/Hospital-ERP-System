import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class CDSSRule(BaseModel):
    __tablename__ = "cdss_rules"

    rule_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. CDSS-SEPSIS-01, CDSS-DRUG-INT-02
    title = Column(String(200), nullable=False)
    # Category: DRUG_INTERACTION, DRUG_ALLERGY, SEPSIS_ALERT, RENAL_DOSAGE, CRITICAL_LAB
    category = Column(String(50), default="DRUG_INTERACTION", nullable=False)
    # Severity: HIGH_CRITICAL, MODERATE, LOW_INFORMATIONAL
    severity = Column(String(30), default="HIGH_CRITICAL", nullable=False)
    description = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    is_active_rule = Column(Boolean, default=True, nullable=False)

class CDSSAlertLog(BaseModel):
    __tablename__ = "cdss_alert_logs"

    rule_id = Column(String(36), ForeignKey("cdss_rules.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    
    alert_message = Column(Text, nullable=False)
    override_reason = Column(Text, nullable=True) # If doctor overrides the alert
    is_overridden = Column(Boolean, default=False, nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    rule = relationship("CDSSRule", lazy="joined")
    patient = relationship("Patient", lazy="joined")
    doctor = relationship("Doctor", lazy="joined")
