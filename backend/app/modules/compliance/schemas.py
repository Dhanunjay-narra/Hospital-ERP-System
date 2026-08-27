from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class DataPrivacyConsentCreate(BaseModel):
    patient_id: str
    compliance_framework: str = "HIPAA"
    purpose_of_processing: str = "Direct Clinical Care & Electronic Billing"
    is_consent_granted: bool = True

class DataPrivacyConsentResponse(DataPrivacyConsentCreate):
    id: str
    consent_timestamp: datetime
    patient: Optional[PatientResponse] = None

    class Config:
        from_attributes = True

class SecurityEventLogCreate(BaseModel):
    event_type: str
    severity: str = "MEDIUM"
    details: str
    ip_address: str = "127.0.0.1"

class SecurityEventLogResponse(SecurityEventLogCreate):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True
