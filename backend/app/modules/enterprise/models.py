import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class BranchTransferRequest(BaseModel):
    __tablename__ = "branch_transfer_requests"

    transfer_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. XFER-2026-0001
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    source_branch_id = Column(String(36), ForeignKey("hospital_branches.id", ondelete="CASCADE"), nullable=False)
    destination_branch_id = Column(String(36), ForeignKey("hospital_branches.id", ondelete="CASCADE"), nullable=False)
    
    clinical_reason = Column(Text, nullable=False) # e.g. Higher-acuity ECMO required, Advanced Neonatal ICU
    requires_advanced_life_support_ambulance = Column(Boolean, default=True, nullable=False)
    
    # STATUS: REQUESTED, APPROVED, AMBULANCE_DISPATCHED, IN_TRANSIT, ARRIVED, COMPLETED, CANCELLED
    status = Column(String(50), default="REQUESTED", index=True, nullable=False)
    authorized_by_user_id = Column(String(36), nullable=True)

    patient = relationship("Patient", lazy="joined")
    source_branch = relationship("HospitalBranch", foreign_keys=[source_branch_id], lazy="joined")
    destination_branch = relationship("HospitalBranch", foreign_keys=[destination_branch_id], lazy="joined")
