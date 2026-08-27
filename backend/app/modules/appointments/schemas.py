from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class AppointmentBase(BaseModel):
    patient_id: str
    doctor_id: str
    department_id: Optional[str] = None
    appointment_date: date
    start_time: str
    end_time: str
    appointment_type: str = "NEW_CONSULTATION"
    booking_channel: str = "WALK_IN"
    chief_complaint: Optional[str] = None
    consultation_fee: float = 100.0

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentStatusUpdate(BaseModel):
    status: str
    cancellation_reason: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: str
    appointment_number: str
    token_number: Optional[int] = None
    status: str
    is_paid: bool
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
