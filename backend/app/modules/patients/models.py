import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, JSON, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Patient(BaseModel):
    __tablename__ = "patients"

    uhid = Column(String(50), unique=True, index=True, nullable=False) # e.g. APX-2026-0001
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False) # MALE, FEMALE, OTHER
    blood_group = Column(String(10), nullable=True) # A+, A-, B+, B-, AB+, AB-, O+, O-
    marital_status = Column(String(30), nullable=True)
    occupation = Column(String(100), nullable=True)
    
    # Contact
    phone_number = Column(String(30), index=True, nullable=False)
    email = Column(String(255), index=True, nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="USA", nullable=True)
    postal_code = Column(String(20), nullable=True)

    # Emergency Contact
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    emergency_contact_phone = Column(String(30), nullable=True)

    # Identification & Insurance
    national_id = Column(String(100), nullable=True)
    passport_number = Column(String(100), nullable=True)
    primary_insurance_provider = Column(String(150), nullable=True)
    insurance_policy_number = Column(String(100), nullable=True)

    # Medical Alerts & Flags
    allergies_summary = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    is_vip = Column(Boolean, default=False, nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False) # ACTIVE, INACTIVE, DECEASED

    # Relationships
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    opd_visits = relationship("OPDVisit", back_populates="patient", cascade="all, delete-orphan")
    admissions = relationship("Admission", back_populates="patient", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="patient", cascade="all, delete-orphan")
    vitals = relationship("VitalSigns", back_populates="patient", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
