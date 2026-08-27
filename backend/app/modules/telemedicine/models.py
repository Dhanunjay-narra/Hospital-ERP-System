import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class TeleconsultationSession(BaseModel):
    __tablename__ = "teleconsultation_sessions"

    session_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. VIRT-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    appointment_id = Column(String(36), ForeignKey("appointments.id", ondelete="SET NULL"), nullable=True)

    scheduled_start = Column(DateTime, nullable=False)
    meeting_room_url = Column(String(500), nullable=False) # e.g. https://telehealth.apexhealth.org/room/VIRT-2026-0001
    call_duration_minutes = Column(Integer, default=0, nullable=False)
    
    # STATUS: SCHEDULED, WAITING_ROOM, IN_CALL, COMPLETED, NO_SHOW, CANCELLED
    status = Column(String(50), default="SCHEDULED", index=True, nullable=False)
    clinical_summary = Column(Text, nullable=True)

    patient = relationship("Patient", lazy="joined")
    doctor = relationship("Doctor", lazy="joined")
