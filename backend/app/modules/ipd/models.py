import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Admission(BaseModel):
    __tablename__ = "admissions"

    admission_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. IPD-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    primary_doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    ward_id = Column(String(36), ForeignKey("wards.id", ondelete="SET NULL"), nullable=True)
    bed_id = Column(String(36), ForeignKey("beds.id", ondelete="SET NULL"), nullable=True)

    admission_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    discharge_date = Column(DateTime, nullable=True)
    
    # ADMISSION_TYPE: EMERGENCY, ELECTIVE, TRANSFER, DAY_CARE
    admission_type = Column(String(50), default="ELECTIVE", nullable=False)
    
    # STATUS: ADMITTED, DISCHARGED, TRANSFERRED_OUT, DECEASED
    status = Column(String(50), default="ADMITTED", index=True, nullable=False)

    admitting_diagnosis = Column(Text, nullable=False)
    discharge_diagnosis = Column(Text, nullable=True)
    attendant_name = Column(String(100), nullable=True)
    attendant_phone = Column(String(30), nullable=True)
    
    # Discharge Details
    discharge_type = Column(String(50), nullable=True) # REGULAR, LAMA (Against Medical Advice), TRANSFER, EXPIRED
    discharge_summary = Column(Text, nullable=True)
    discharge_instructions = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="admissions", lazy="joined")
    primary_doctor = relationship("Doctor", lazy="joined")
    ward = relationship("Ward", lazy="joined")
    bed = relationship("Bed", lazy="joined")
    daily_rounds = relationship("DailyClinicalRound", back_populates="admission", cascade="all, delete-orphan")

class DailyClinicalRound(BaseModel):
    __tablename__ = "daily_clinical_rounds"

    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    round_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    clinical_observations = Column(Text, nullable=False)
    treatment_orders = Column(Text, nullable=True)
    nursing_instructions = Column(Text, nullable=True)
    dietary_orders = Column(String(150), nullable=True) # e.g. Diabetic soft diet, NPO
    fluid_orders = Column(String(150), nullable=True)

    admission = relationship("Admission", back_populates="daily_rounds")
    doctor = relationship("Doctor", lazy="joined")
