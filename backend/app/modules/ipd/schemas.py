from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse
from app.modules.organization.schemas import WardResponse, BedResponse

class DailyClinicalRoundBase(BaseModel):
    doctor_id: str
    clinical_observations: str
    treatment_orders: Optional[str] = None
    nursing_instructions: Optional[str] = None
    dietary_orders: Optional[str] = None

class DailyClinicalRoundCreate(DailyClinicalRoundBase):
    admission_id: str

class DailyClinicalRoundResponse(DailyClinicalRoundBase):
    id: str
    round_datetime: datetime
    doctor: Optional[DoctorResponse] = None

    class Config:
        from_attributes = True

class AdmissionBase(BaseModel):
    patient_id: str
    primary_doctor_id: str
    department_id: Optional[str] = None
    ward_id: Optional[str] = None
    bed_id: Optional[str] = None
    admission_type: str = "ELECTIVE"
    admitting_diagnosis: str
    attendant_name: Optional[str] = None
    attendant_phone: Optional[str] = None

class AdmissionCreate(AdmissionBase):
    pass

class DischargeRequest(BaseModel):
    discharge_type: str = "REGULAR" # REGULAR, LAMA, TRANSFER, EXPIRED
    discharge_diagnosis: str
    discharge_summary: str
    discharge_instructions: Optional[str] = None

class AdmissionResponse(AdmissionBase):
    id: str
    admission_number: str
    admission_date: datetime
    discharge_date: Optional[datetime] = None
    status: str
    patient: Optional[PatientResponse] = None
    primary_doctor: Optional[DoctorResponse] = None
    ward: Optional[WardResponse] = None
    bed: Optional[BedResponse] = None
    daily_rounds: List[DailyClinicalRoundResponse] = []

    class Config:
        from_attributes = True
