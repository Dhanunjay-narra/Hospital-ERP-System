import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class BloodDonor(BaseModel):
    __tablename__ = "blood_donors"

    donor_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. DONOR-2026-001
    full_name = Column(String(150), nullable=False)
    gender = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    blood_group = Column(String(10), nullable=False) # A+, O+, etc.
    phone_number = Column(String(30), nullable=False)
    email = Column(String(255), nullable=True)
    
    last_donation_date = Column(Date, nullable=True)
    is_eligible = Column(Boolean, default=True, nullable=False)
    hemoglobin_level = Column(Float, default=13.5, nullable=False) # g/dL

    units = relationship("BloodUnit", back_populates="donor", cascade="all, delete-orphan")

class BloodUnit(BaseModel):
    __tablename__ = "blood_units"

    unit_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. UNIT-O-POS-9981
    donor_id = Column(String(36), ForeignKey("blood_donors.id", ondelete="SET NULL"), nullable=True)
    blood_group = Column(String(10), index=True, nullable=False)
    
    # Component: WHOLE_BLOOD, PRBC (Packed Red Blood Cells), FFP (Fresh Frozen Plasma), PLATELETS, CRYOPRECIPITATE
    component_type = Column(String(50), default="PRBC", nullable=False)
    volume_ml = Column(Float, default=350.0, nullable=False)
    collection_date = Column(Date, nullable=False)
    expiry_date = Column(Date, index=True, nullable=False)
    
    storage_refrigerator_id = Column(String(50), default="REF-COLD-1 (4°C)", nullable=False)
    
    # STATUS: AVAILABLE, RESERVED, ISSUED, EXPIRED, DISCARDED
    status = Column(String(30), default="AVAILABLE", index=True, nullable=False)
    reserved_patient_id = Column(String(36), nullable=True)

    donor = relationship("BloodDonor", back_populates="units", lazy="joined")
