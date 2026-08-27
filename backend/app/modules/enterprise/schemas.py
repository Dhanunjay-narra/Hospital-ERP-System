from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.organization.schemas import HospitalBranchResponse

class BranchTransferCreate(BaseModel):
    patient_id: str
    source_branch_id: str
    destination_branch_id: str
    clinical_reason: str
    requires_advanced_life_support_ambulance: bool = True

class BranchTransferResponse(BranchTransferCreate):
    id: str
    transfer_code: str
    status: str
    patient: Optional[PatientResponse] = None
    source_branch: Optional[HospitalBranchResponse] = None
    destination_branch: Optional[HospitalBranchResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
