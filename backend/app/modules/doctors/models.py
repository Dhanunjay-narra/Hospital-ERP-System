import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, JSON, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Doctor(BaseModel):
    __tablename__ = "doctors"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doctor_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. DOC-101
    license_number = Column(String(100), unique=True, nullable=False)
    specialization = Column(String(150), nullable=False) # Cardiology, Neurology, Pediatrics, etc.
    sub_specialties = Column(String(255), nullable=True)
    qualification = Column(String(200), nullable=False) # MBBS, MD, FRCS, etc.
    experience_years = Column(Integer, default=0, nullable=False)
    
    # Department & Consultation
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    consultation_room = Column(String(50), nullable=True)
    consultation_fee = Column(Float, default=100.0, nullable=False)
    follow_up_fee = Column(Float, default=50.0, nullable=False)
    follow_up_validity_days = Column(Integer, default=7, nullable=False)
    slot_duration_minutes = Column(Integer, default=15, nullable=False)
    
    bio = Column(Text, nullable=True)
    is_available_for_teleconsult = Column(Boolean, default=False, nullable=False)
    is_on_duty = Column(Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", lazy="joined")
    schedules = relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor")
    opd_visits = relationship("OPDVisit", back_populates="doctor")

class DoctorSchedule(BaseModel):
    __tablename__ = "doctor_schedules"

    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0=Monday, 6=Sunday
    start_time = Column(String(10), nullable=False) # "09:00"
    end_time = Column(String(10), nullable=False) # "17:00"
    max_patients = Column(Integer, default=30, nullable=False)
    is_active_day = Column(Boolean, default=True, nullable=False)

    doctor = relationship("Doctor", back_populates="schedules")
