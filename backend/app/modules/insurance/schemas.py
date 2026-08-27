from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse

class InsuranceProviderBase(BaseModel):
    name: str
    code: str
    tpa_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    portal_url: Optional[str] = None

class InsuranceProviderCreate(InsuranceProviderBase):
    pass

class InsuranceProviderResponse(InsuranceProviderBase):
    id: str

    class Config:
        from_attributes = True

class InsuranceClaimCreate(BaseModel):
    patient_id: str
    provider_id: str
    invoice_id: Optional[str] = None
    admission_id: Optional[str] = None
    policy_number: str
    pre_auth_number: Optional[str] = None
    total_claim_amount: float

class InsuranceClaimResponse(InsuranceClaimCreate):
    id: str
    claim_number: str
    approved_amount: float
    patient_copay_amount: float
    deduction_amount: float
    status: str
    submission_date: datetime
    patient: Optional[PatientResponse] = None
    provider: Optional[InsuranceProviderResponse] = None

    class Config:
        from_attributes = True
