import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class MedicationAdministrationRecord(BaseModel):
    __tablename__ = "medication_administration_records"

    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="CASCADE"), nullable=False)
    prescription_item_id = Column(String(36), ForeignKey("prescription_items.id", ondelete="SET NULL"), nullable=True)
    medicine_name = Column(String(200), nullable=False)
    dosage = Column(String(50), nullable=False)
    route = Column(String(50), default="ORAL", nullable=False)
    
    scheduled_time = Column(DateTime, nullable=False)
    administered_time = Column(DateTime, nullable=True)
    administered_by_nurse_id = Column(String(36), nullable=True)
    
    # STATUS: GIVEN, MISSED, REFUSED, HELD
    status = Column(String(30), default="SCHEDULED", nullable=False)
    notes = Column(Text, nullable=True)

class NursingNote(BaseModel):
    __tablename__ = "nursing_notes"

    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="CASCADE"), nullable=False)
    nurse_id = Column(String(36), nullable=False)
    shift_type = Column(String(30), default="DAY", nullable=False) # MORNING, EVENING, NIGHT
    note_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    observations = Column(Text, nullable=False)
    interventions = Column(Text, nullable=True)
    patient_response = Column(Text, nullable=True)
    handover_instructions = Column(Text, nullable=True)

class IntakeOutputChart(BaseModel):
    __tablename__ = "intake_output_charts"

    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="CASCADE"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    recorded_by = Column(String(36), nullable=True)
    
    # Intake (mL)
    oral_intake_ml = Column(Float, default=0.0, nullable=False)
    iv_fluids_ml = Column(Float, default=0.0, nullable=False)
    ng_tube_ml = Column(Float, default=0.0, nullable=False)
    total_intake_ml = Column(Float, default=0.0, nullable=False)

    # Output (mL)
    urine_output_ml = Column(Float, default=0.0, nullable=False)
    drain_output_ml = Column(Float, default=0.0, nullable=False)
    vomitus_ml = Column(Float, default=0.0, nullable=False)
    stool_count = Column(Integer, default=0, nullable=False)
    total_output_ml = Column(Float, default=0.0, nullable=False)

    balance_ml = Column(Float, default=0.0, nullable=False)
