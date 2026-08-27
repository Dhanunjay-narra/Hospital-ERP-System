import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class PatientLead(BaseModel):
    __tablename__ = "patient_leads"

    lead_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. LEAD-2026-0001
    full_name = Column(String(150), nullable=False)
    phone_number = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    
    # Source: WEBSITE, SOCIAL_MEDIA, DOCTOR_REFERRAL, HEALTH_CAMP, WALK_IN
    lead_source = Column(String(50), default="WEBSITE", nullable=False)
    inquiry_specialty = Column(String(100), default="Cardiology", nullable=False)
    notes = Column(Text, nullable=True)
    
    # STATUS: NEW, CONTACTED, QUALIFIED, APPOINTMENT_BOOKED, CONVERTED, LOST
    status = Column(String(50), default="NEW", index=True, nullable=False)
    converted_patient_id = Column(String(36), ForeignKey("patients.id", ondelete="SET NULL"), nullable=True)
    assigned_counselor_id = Column(String(36), nullable=True)

    converted_patient = relationship("Patient", lazy="joined")
    interactions = relationship("LeadInteraction", back_populates="lead", cascade="all, delete-orphan", lazy="joined")

class LeadInteraction(BaseModel):
    __tablename__ = "lead_interactions"

    lead_id = Column(String(36), ForeignKey("patient_leads.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String(50), default="PHONE_CALL", nullable=False) # PHONE_CALL, WHATSAPP, EMAIL, IN_PERSON
    summary = Column(Text, nullable=False)
    next_follow_up = Column(DateTime, nullable=True)
    counselor_user_id = Column(String(36), nullable=True)

    lead = relationship("PatientLead", back_populates="interactions")
