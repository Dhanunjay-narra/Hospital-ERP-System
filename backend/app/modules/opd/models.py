import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class OPDVisit(BaseModel):
    __tablename__ = "opd_visits"

    visit_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. OPD-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    appointment_id = Column(String(36), ForeignKey("appointments.id", ondelete="SET NULL"), nullable=True)

    visit_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    queue_number = Column(Integer, nullable=True)
    
    # Status: WAITING, IN_CONSULTATION, COMPLETED, CANCELLED
    status = Column(String(50), default="WAITING", nullable=False)
    
    # Clinical consultation summary
    chief_complaint = Column(Text, nullable=True)
    history_of_present_illness = Column(Text, nullable=True)
    physical_examination = Column(Text, nullable=True)
    provisional_diagnosis = Column(Text, nullable=True)
    final_diagnosis = Column(Text, nullable=True)
    icd10_code = Column(String(50), nullable=True)
    treatment_plan = Column(Text, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    doctor_notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="opd_visits", lazy="joined")
    doctor = relationship("Doctor", back_populates="opd_visits", lazy="joined")
    appointment = relationship("Appointment", back_populates="opd_visit")
    vitals = relationship("VitalSigns", back_populates="opd_visit", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="opd_visit", cascade="all, delete-orphan")

class VitalSigns(BaseModel):
    __tablename__ = "vital_signs"

    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    opd_visit_id = Column(String(36), ForeignKey("opd_visits.id", ondelete="SET NULL"), nullable=True)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    recorded_by = Column(String(36), nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Vitals metrics
    systolic_bp = Column(Integer, nullable=True) # mmHg e.g. 120
    diastolic_bp = Column(Integer, nullable=True) # mmHg e.g. 80
    pulse_rate = Column(Integer, nullable=True) # bpm e.g. 72
    respiratory_rate = Column(Integer, nullable=True) # breaths/min e.g. 16
    temperature_celsius = Column(Float, nullable=True) # °C e.g. 37.0
    spo2_percentage = Column(Float, nullable=True) # % e.g. 98.5
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    blood_glucose_random = Column(Float, nullable=True) # mg/dL
    pain_score = Column(Integer, nullable=True) # 0-10
    notes = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="vitals")
    opd_visit = relationship("OPDVisit", back_populates="vitals")
