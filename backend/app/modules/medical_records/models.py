import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class MedicalRecordArchive(BaseModel):
    __tablename__ = "medical_record_archives"

    archive_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. MRD-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    
    physical_rack_number = Column(String(50), default="Rack-B-Section-4", nullable=False)
    total_file_pages = Column(Integer, default=24, nullable=False)
    retention_period_years = Column(Integer, default=10, nullable=False)
    
    # STATUS: ARCHIVED, CHECKED_OUT, IN_LEGAL_REVIEW, DESTROYED
    status = Column(String(30), default="ARCHIVED", index=True, nullable=False)
    archived_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("Patient", lazy="joined")
    admission = relationship("Admission", lazy="joined")

class RecordAccessLog(BaseModel):
    __tablename__ = "record_access_logs"

    archive_id = Column(String(36), ForeignKey("medical_record_archives.id", ondelete="CASCADE"), nullable=False)
    accessed_by_user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    purpose = Column(String(255), nullable=False) # Clinical Review, Legal Request, Insurance Audit, Research
    access_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    archive = relationship("MedicalRecordArchive", lazy="joined")
    user = relationship("User", lazy="joined")
