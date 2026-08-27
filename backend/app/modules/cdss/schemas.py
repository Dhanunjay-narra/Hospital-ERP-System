from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class CDSSRuleBase(BaseModel):
    rule_code: str
    title: str
    category: str = "DRUG_INTERACTION"
    severity: str = "HIGH_CRITICAL"
    description: str
    recommended_action: str
    is_active_rule: bool = True

class CDSSRuleCreate(CDSSRuleBase):
    pass

class CDSSRuleResponse(CDSSRuleBase):
    id: str

    class Config:
        from_attributes = True

class CDSSAlertCreate(BaseModel):
    rule_id: str
    patient_id: str
    doctor_id: str
    alert_message: str
    override_reason: Optional[str] = None
    is_overridden: bool = False

class CDSSAlertResponse(CDSSAlertCreate):
    id: str
    triggered_at: datetime
    rule: Optional[CDSSRuleResponse] = None
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None

    class Config:
        from_attributes = True
