import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class OTRoom(BaseModel):
    __tablename__ = "ot_rooms"

    name = Column(String(100), nullable=False) # e.g. Major OT 1 (Cardiac), Minor OT 2 (Ortho)
    code = Column(String(50), unique=True, nullable=False)
    ot_type = Column(String(50), default="MAJOR", nullable=False) # MAJOR, MINOR, CARDIAC, NEURO, ROBOTIC
    status = Column(String(30), default="AVAILABLE", nullable=False) # AVAILABLE, IN_SURGERY, CLEANING, MAINTENANCE

    surgeries = relationship("SurgeryBooking", back_populates="ot_room")

class SurgeryBooking(BaseModel):
    __tablename__ = "surgery_bookings"

    surgery_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. SURG-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    ot_room_id = Column(String(36), ForeignKey("ot_rooms.id", ondelete="CASCADE"), nullable=False)
    lead_surgeon_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    anesthetist_id = Column(String(36), ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True)

    procedure_name = Column(String(255), nullable=False) # e.g. Coronary Artery Bypass Graft (CABG), Total Knee Replacement
    procedure_code = Column(String(50), nullable=True)
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)

    anesthesia_type = Column(String(50), default="GENERAL", nullable=False) # GENERAL, SPINAL, EPIDURAL, LOCAL, SEDATION
    
    # STATUS: SCHEDULED, PRE_OP, IN_SURGERY, RECOVERY, COMPLETED, CANCELLED
    status = Column(String(50), default="SCHEDULED", index=True, nullable=False)
    
    # Surgical Safety Checklists (WHO)
    sign_in_completed = Column(Boolean, default=False, nullable=False)
    time_out_completed = Column(Boolean, default=False, nullable=False)
    sign_out_completed = Column(Boolean, default=False, nullable=False)
    
    pre_op_diagnosis = Column(Text, nullable=True)
    post_op_diagnosis = Column(Text, nullable=True)
    operative_findings = Column(Text, nullable=True)
    implants_used = Column(Text, nullable=True)
    post_op_orders = Column(Text, nullable=True)

    patient = relationship("Patient", lazy="joined")
    lead_surgeon = relationship("Doctor", foreign_keys=[lead_surgeon_id], lazy="joined")
    anesthetist = relationship("Doctor", foreign_keys=[anesthetist_id], lazy="joined")
    ot_room = relationship("OTRoom", back_populates="surgeries", lazy="joined")
