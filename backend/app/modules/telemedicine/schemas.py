from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class TeleconsultationCreate(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    scheduled_start: datetime

class TeleconsultationResponse(TeleconsultationCreate):
    id: str
    session_code: str
    meeting_room_url: str
    call_duration_minutes: int
    status: str
    clinical_summary: Optional[str] = None
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
