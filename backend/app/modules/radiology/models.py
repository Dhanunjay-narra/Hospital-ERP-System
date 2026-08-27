import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class RadiologyOrder(BaseModel):
    __tablename__ = "radiology_orders"

    order_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. RAD-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)

    modality = Column(String(50), nullable=False) # X_RAY, CT_SCAN, MRI, ULTRASOUND, MAMMOGRAPHY
    procedure_name = Column(String(200), nullable=False) # e.g. Chest X-Ray PA View, CT Brain Non-Contrast
    clinical_indication = Column(Text, nullable=True)
    
    # STATUS: ORDERED, SCHEDULED, PERFORMED, REPORTED, APPROVED
    status = Column(String(50), default="ORDERED", index=True, nullable=False)
    
    # PACS / DICOM Integration links
    dicom_study_uid = Column(String(150), nullable=True)
    pacs_image_url = Column(String(500), nullable=True)
    
    # Radiologist Report
    radiologist_id = Column(String(36), nullable=True)
    radiology_findings = Column(Text, nullable=True)
    impression = Column(Text, nullable=True)
    reported_at = Column(DateTime, nullable=True)
    is_critical_finding = Column(Boolean, default=False, nullable=False)

    patient = relationship("Patient", lazy="joined")
    doctor = relationship("Doctor", lazy="joined")
