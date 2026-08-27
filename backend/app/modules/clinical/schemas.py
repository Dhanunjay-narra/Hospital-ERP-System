from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class AllergyCreate(BaseModel):
    patient_id: str
    allergen_type: str = "DRUG"
    allergen_name: str
    severity: str = "MODERATE"
    reaction: Optional[str] = None

class AllergyResponse(AllergyCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class PrescriptionItemBase(BaseModel):
    medicine_name: str
    generic_name: Optional[str] = None
    dosage: str
    frequency: str
    duration_days: int = 5
    route: str = "ORAL"
    timing_instructions: Optional[str] = "After Food"
    total_quantity: int = 10

class PrescriptionItemCreate(PrescriptionItemBase):
    pass

class PrescriptionItemResponse(PrescriptionItemBase):
    id: str
    dispensed_quantity: int
    is_dispensed: bool

    class Config:
        from_attributes = True

class PrescriptionBase(BaseModel):
    patient_id: str
    doctor_id: str
    opd_visit_id: Optional[str] = None
    admission_id: Optional[str] = None
    diagnosis_notes: Optional[str] = None
    general_advice: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    items: List[PrescriptionItemCreate]

class PrescriptionResponse(PrescriptionBase):
    id: str
    prescription_number: str
    issued_date: datetime
    status: str
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    items: List[PrescriptionItemResponse] = []

    class Config:
        from_attributes = True
