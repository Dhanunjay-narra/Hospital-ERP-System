from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class VitalSignsBase(BaseModel):
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    pulse_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature_celsius: Optional[float] = None
    spo2_percentage: Optional[float] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    blood_glucose_random: Optional[float] = None
    pain_score: Optional[int] = None
    notes: Optional[str] = None

class VitalSignsCreate(VitalSignsBase):
    patient_id: str
    opd_visit_id: Optional[str] = None
    admission_id: Optional[str] = None

class VitalSignsResponse(VitalSignsBase):
    id: str
    patient_id: str
    bmi: Optional[float] = None
    recorded_at: datetime

    class Config:
        from_attributes = True

class OPDVisitBase(BaseModel):
    patient_id: str
    doctor_id: str
    department_id: Optional[str] = None
    appointment_id: Optional[str] = None
    chief_complaint: Optional[str] = None

class OPDVisitCreate(OPDVisitBase):
    pass

class OPDConsultationUpdate(BaseModel):
    status: Optional[str] = "COMPLETED"
    history_of_present_illness: Optional[str] = None
    physical_examination: Optional[str] = None
    provisional_diagnosis: Optional[str] = None
    final_diagnosis: Optional[str] = None
    icd10_code: Optional[str] = None
    treatment_plan: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    doctor_notes: Optional[str] = None

class OPDVisitResponse(OPDVisitBase):
    id: str
    visit_number: str
    queue_number: Optional[int] = None
    status: str
    visit_datetime: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    vitals: List[VitalSignsResponse] = []
    final_diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None

    class Config:
        from_attributes = True
