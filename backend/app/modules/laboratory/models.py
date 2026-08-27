import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class LabTestCatalog(BaseModel):
    __tablename__ = "lab_test_catalog"

    test_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. CBC, LFT, KFT, LIPID, TSH
    test_name = Column(String(200), nullable=False) # Complete Blood Count
    department = Column(String(100), default="HEMATOLOGY", nullable=False) # HEMATOLOGY, BIOCHEMISTRY, MICROBIOLOGY, PATHOLOGY
    sample_type = Column(String(50), default="WHOLE_BLOOD", nullable=False) # WHOLE_BLOOD, SERUM, URINE, CSF, STOOL
    turnaround_time_hours = Column(Integer, default=4, nullable=False)
    price = Column(Float, default=50.0, nullable=False)
    
    # Reference Ranges & Critical Panic Values
    unit_of_measure = Column(String(50), nullable=True) # g/dL, mg/dL, mmol/L, %
    reference_min = Column(Float, nullable=True)
    reference_max = Column(Float, nullable=True)
    critical_low = Column(Float, nullable=True)
    critical_high = Column(Float, nullable=True)

class LabOrder(BaseModel):
    __tablename__ = "lab_orders"

    order_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. LAB-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    opd_visit_id = Column(String(36), ForeignKey("opd_visits.id", ondelete="SET NULL"), nullable=True)

    order_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    priority = Column(String(20), default="ROUTINE", nullable=False) # ROUTINE, URGENT, STAT / EMERGENCY
    
    # STATUS: ORDERED, SAMPLE_COLLECTED, IN_PROCESSING, RESULTED, VALIDATED, CANCELLED
    status = Column(String(50), default="ORDERED", index=True, nullable=False)
    sample_barcode = Column(String(100), nullable=True)
    collected_at = Column(DateTime, nullable=True)
    technician_id = Column(String(36), nullable=True)
    validated_by_id = Column(String(36), nullable=True)

    patient = relationship("Patient", lazy="joined")
    doctor = relationship("Doctor", lazy="joined")
    results = relationship("LabResult", back_populates="order", cascade="all, delete-orphan", lazy="joined")

class LabResult(BaseModel):
    __tablename__ = "lab_results"

    lab_order_id = Column(String(36), ForeignKey("lab_orders.id", ondelete="CASCADE"), nullable=False)
    test_id = Column(String(36), ForeignKey("lab_test_catalog.id", ondelete="CASCADE"), nullable=False)
    parameter_name = Column(String(150), nullable=False) # e.g. Hemoglobin, White Blood Cells, Potassium
    result_value = Column(String(100), nullable=False) # e.g. "14.2" or "Negative"
    numeric_value = Column(Float, nullable=True)
    unit_of_measure = Column(String(50), nullable=True)
    reference_range = Column(String(100), nullable=True) # e.g. "12.0 - 16.0"
    
    is_abnormal = Column(Boolean, default=False, nullable=False)
    is_critical = Column(Boolean, default=False, nullable=False) # Panic value alert
    technician_remarks = Column(Text, nullable=True)

    order = relationship("LabOrder", back_populates="results")
    test = relationship("LabTestCatalog", lazy="joined")
