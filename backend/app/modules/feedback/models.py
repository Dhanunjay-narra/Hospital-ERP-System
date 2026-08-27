import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class PatientFeedback(BaseModel):
    __tablename__ = "patient_feedbacks"

    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    admission_id = Column(String(36), ForeignKey("admissions.id", ondelete="SET NULL"), nullable=True)
    opd_visit_id = Column(String(36), ForeignKey("opd_visits.id", ondelete="SET NULL"), nullable=True)

    # Net Promoter Score: 0 - 10 (9-10 Promoter, 7-8 Passive, 0-6 Detractor)
    nps_score = Column(Integer, nullable=False)
    doctor_care_rating = Column(Integer, default=5, nullable=False) # 1 - 5
    nursing_care_rating = Column(Integer, default=5, nullable=False) # 1 - 5
    cleanliness_rating = Column(Integer, default=5, nullable=False) # 1 - 5
    billing_experience_rating = Column(Integer, default=5, nullable=False) # 1 - 5
    
    comments = Column(Text, nullable=True)
    is_grievance = Column(Boolean, default=False, nullable=False)
    grievance_resolved = Column(Boolean, default=False, nullable=False)

    patient = relationship("Patient", lazy="joined")
