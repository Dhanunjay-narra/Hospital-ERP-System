from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class EmergencyTriageCreate(BaseModel):
    patient_id: str
    priority_level: str = "YELLOW" # RED, AMBER, YELLOW, GREEN, BLUE
    chief_complaint: str
    mechanism_of_injury: Optional[str] = None
    glasgow_coma_scale: Optional[int] = 15
    airway_compromised: bool = False
    breathing_difficulty: bool = False
    circulatory_shock: bool = False
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    pulse_rate: Optional[int] = None
    spo2_percentage: Optional[float] = None
    temperature_celsius: Optional[float] = None
    assigned_bay: Optional[str] = "Trauma Bay 1"

class EmergencyTriageResponse(EmergencyTriageCreate):
    id: str
    triage_number: str
    status: str
    created_at: datetime
    patient: Optional[PatientResponse] = None

    class Config:
        from_attributes = True
