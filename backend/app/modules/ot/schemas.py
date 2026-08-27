from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class OTRoomBase(BaseModel):
    name: str
    code: str
    ot_type: str = "MAJOR"
    status: str = "AVAILABLE"

class OTRoomCreate(OTRoomBase):
    pass

class OTRoomResponse(OTRoomBase):
    id: str

    class Config:
        from_attributes = True

class SurgeryBookingCreate(BaseModel):
    patient_id: str
    admission_id: Optional[str] = None
    ot_room_id: str
    lead_surgeon_id: str
    anesthetist_id: Optional[str] = None
    procedure_name: str
    procedure_code: Optional[str] = None
    scheduled_start: datetime
    scheduled_end: datetime
    anesthesia_type: str = "GENERAL"
    pre_op_diagnosis: Optional[str] = None

class SurgeryBookingResponse(SurgeryBookingCreate):
    id: str
    surgery_number: str
    status: str
    sign_in_completed: bool
    time_out_completed: bool
    sign_out_completed: bool
    patient: Optional[PatientResponse] = None
    lead_surgeon: Optional[DoctorResponse] = None
    ot_room: Optional[OTRoomResponse] = None

    class Config:
        from_attributes = True
