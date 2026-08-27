import uuid
from datetime import datetime, date, time
from sqlalchemy import Column, String, Boolean, DateTime, Date, Time, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Appointment(BaseModel):
    __tablename__ = "appointments"

    appointment_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. APT-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    appointment_date = Column(Date, index=True, nullable=False)
    start_time = Column(String(10), nullable=False) # "10:30"
    end_time = Column(String(10), nullable=False) # "10:45"
    token_number = Column(Integer, nullable=True)

    # Type & Source
    appointment_type = Column(String(50), default="NEW_CONSULTATION", nullable=False) # NEW_CONSULTATION, FOLLOW_UP, EMERGENCY, TELEMEDICINE
    booking_channel = Column(String(50), default="WALK_IN", nullable=False) # WALK_IN, ONLINE, CALL_CENTER, REFERRAL

    # Status Lifecycle: REQUESTED -> CONFIRMED -> CHECKED_IN -> WAITING -> CONSULTATION -> COMPLETED / CANCELLED / NO_SHOW
    status = Column(String(50), default="CONFIRMED", index=True, nullable=False)
    
    chief_complaint = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    consultation_fee = Column(Float, default=100.0, nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="appointments", lazy="joined")
    doctor = relationship("Doctor", back_populates="appointments", lazy="joined")
    opd_visit = relationship("OPDVisit", back_populates="appointment", uselist=False)
