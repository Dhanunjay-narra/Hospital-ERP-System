import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class EmergencyTriage(BaseModel):
    __tablename__ = "emergency_triages"

    triage_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. ER-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    
    # Priority classification: RED (Immediate / Resuscitation), AMBER (Very Urgent < 10min), YELLOW (Urgent < 60min), GREEN (Standard), BLUE (Non-urgent)
    priority_level = Column(String(20), default="YELLOW", index=True, nullable=False)
    chief_complaint = Column(Text, nullable=False)
    mechanism_of_injury = Column(Text, nullable=True)
    glasgow_coma_scale = Column(Integer, nullable=True) # 3 - 15
    airway_compromised = Column(Boolean, default=False, nullable=False)
    breathing_difficulty = Column(Boolean, default=False, nullable=False)
    circulatory_shock = Column(Boolean, default=False, nullable=False)
    
    # Initial vitals
    systolic_bp = Column(Integer, nullable=True)
    diastolic_bp = Column(Integer, nullable=True)
    pulse_rate = Column(Integer, nullable=True)
    spo2_percentage = Column(Float, nullable=True)
    temperature_celsius = Column(Float, nullable=True)
    
    assigned_bay = Column(String(50), nullable=True) # Resus Bay 1, Trauma Bay 2
    assigned_physician_id = Column(String(36), nullable=True)
    
    # STATUS: TRIAGED, IN_TREATMENT, ADMITTED_IPD, DISCHARGED, EXPIRED
    status = Column(String(50), default="TRIAGED", index=True, nullable=False)
    disposition_notes = Column(Text, nullable=True)

    patient = relationship("Patient", lazy="joined")
