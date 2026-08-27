from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class PatientFeedbackBase(BaseModel):
    patient_id: str
    admission_id: Optional[str] = None
    opd_visit_id: Optional[str] = None
    nps_score: int # 0 - 10
    doctor_care_rating: int = 5
    nursing_care_rating: int = 5
    cleanliness_rating: int = 5
    billing_experience_rating: int = 5
    comments: Optional[str] = None
    is_grievance: bool = False

class PatientFeedbackCreate(PatientFeedbackBase):
    pass

class PatientFeedbackResponse(PatientFeedbackBase):
    id: str
    grievance_resolved: bool
    patient: Optional[PatientResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
