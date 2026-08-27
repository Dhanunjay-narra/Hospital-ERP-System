from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class LeadInteractionCreate(BaseModel):
    channel: str = "PHONE_CALL"
    summary: str
    next_follow_up: Optional[datetime] = None

class LeadInteractionResponse(LeadInteractionCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class PatientLeadBase(BaseModel):
    full_name: str
    phone_number: str
    email: Optional[str] = None
    city: Optional[str] = None
    lead_source: str = "WEBSITE"
    inquiry_specialty: str = "Cardiology"
    notes: Optional[str] = None

class PatientLeadCreate(PatientLeadBase):
    pass

class PatientLeadResponse(PatientLeadBase):
    id: str
    lead_code: str
    status: str
    converted_patient: Optional[PatientResponse] = None
    interactions: List[LeadInteractionResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
