from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class PatientDocumentBase(BaseModel):
    patient_id: str
    admission_id: Optional[str] = None
    document_title: str
    category: str = "CONSENT_FORM" # CONSENT_FORM, IDENTITY_PROOF, INSURANCE_CARD, DISCHARGE_SUMMARY
    file_path: str = "/storage/docs/sample.pdf"
    file_size_kb: int = 150
    mime_type: str = "application/pdf"
    is_digitally_signed: bool = True
    signed_by_name: Optional[str] = None

class PatientDocumentCreate(PatientDocumentBase):
    pass

class PatientDocumentResponse(PatientDocumentBase):
    id: str
    signed_at: Optional[datetime] = None
    patient: Optional[PatientResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
