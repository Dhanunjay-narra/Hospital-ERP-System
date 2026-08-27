from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class MedicalRecordArchiveBase(BaseModel):
    patient_id: str
    admission_id: Optional[str] = None
    physical_rack_number: str = "Rack-B-Section-4"
    total_file_pages: int = 24
    retention_period_years: int = 10

class MedicalRecordArchiveCreate(MedicalRecordArchiveBase):
    pass

class MedicalRecordArchiveResponse(MedicalRecordArchiveBase):
    id: str
    archive_code: str
    status: str
    archived_date: datetime
    patient: Optional[PatientResponse] = None

    class Config:
        from_attributes = True

class RecordAccessLogCreate(BaseModel):
    archive_id: str
    purpose: str

class RecordAccessLogResponse(RecordAccessLogCreate):
    id: str
    accessed_by_user_id: str
    access_time: datetime

    class Config:
        from_attributes = True
