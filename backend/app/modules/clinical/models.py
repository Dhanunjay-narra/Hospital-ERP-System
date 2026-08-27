import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Allergy(BaseModel):
    __tablename__ = "allergies"

    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    allergen_type = Column(String(50), default="DRUG", nullable=False) # DRUG, FOOD, ENVIRONMENTAL
    allergen_name = Column(String(150), nullable=False) # e.g. Penicillin, Peanuts, Latex
    severity = Column(String(30), default="MODERATE", nullable=False) # MILD, MODERATE, SEVERE, LIFE_THREATENING
    reaction = Column(String(255), nullable=True) # e.g. Anaphylaxis, Rash, Angioedema

class Prescription(BaseModel):
    __tablename__ = "prescriptions"

    prescription_number = Column(String(50), unique=True, index=True, nullable=False)
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    opd_visit_id = Column(String(36), ForeignKey("opd_visits.id", ondelete="SET NULL"), nullable=True)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    
    issued_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    diagnosis_notes = Column(Text, nullable=True)
    general_advice = Column(Text, nullable=True)
    
    # STATUS: PENDING_DISPENSE, PARTIALLY_DISPENSED, DISPENSED, CANCELLED
    status = Column(String(50), default="PENDING_DISPENSE", nullable=False)

    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", lazy="joined")
    opd_visit = relationship("OPDVisit", back_populates="prescriptions")
    items = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan", lazy="joined")

class PrescriptionItem(BaseModel):
    __tablename__ = "prescription_items"

    prescription_id = Column(String(36), ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    medicine_name = Column(String(200), nullable=False) # e.g. Amoxicillin 500mg
    generic_name = Column(String(200), nullable=True)
    dosage = Column(String(50), nullable=False) # e.g. 500mg, 1 tablet
    frequency = Column(String(50), nullable=False) # 1-0-1, 1-1-1, Once Daily, PRN
    duration_days = Column(Integer, default=5, nullable=False)
    route = Column(String(50), default="ORAL", nullable=False) # ORAL, IV, IM, TOPICAL, INHALATION
    timing_instructions = Column(String(100), default="After Food", nullable=True) # Before Food, After Food
    total_quantity = Column(Integer, default=10, nullable=False)
    dispensed_quantity = Column(Integer, default=0, nullable=False)
    is_dispensed = Column(Boolean, default=False, nullable=False)

    prescription = relationship("Prescription", back_populates="items")
