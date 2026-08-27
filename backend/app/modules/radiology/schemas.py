from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class RadiologyOrderCreate(BaseModel):
    patient_id: str
    doctor_id: str
    admission_id: Optional[str] = None
    modality: str = "X_RAY" # X_RAY, CT_SCAN, MRI, ULTRASOUND
    procedure_name: str
    clinical_indication: Optional[str] = None

class RadiologyReportSubmit(BaseModel):
    radiology_findings: str
    impression: str
    is_critical_finding: bool = False
    pacs_image_url: Optional[str] = None

class RadiologyOrderResponse(RadiologyOrderCreate):
    id: str
    order_number: str
    status: str
    radiology_findings: Optional[str] = None
    impression: Optional[str] = None
    is_critical_finding: bool = False
    pacs_image_url: Optional[str] = None
    reported_at: Optional[datetime] = None
    created_at: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None

    class Config:
        from_attributes = True
