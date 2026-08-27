from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    occupation: Optional[str] = None
    phone_number: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "USA"
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    primary_insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    allergies_summary: Optional[str] = None
    chronic_conditions: Optional[str] = None
    is_vip: bool = False

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    allergies_summary: Optional[str] = None
    chronic_conditions: Optional[str] = None
    status: Optional[str] = None

class PatientResponse(PatientBase):
    id: str
    uhid: str
    age: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class Patient360Summary(BaseModel):
    patient: PatientResponse
    total_appointments: int
    total_opd_visits: int
    total_admissions: int
    active_prescriptions_count: int
    recent_vitals: Optional[Dict[str, Any]] = None
    recent_allergies: List[str] = []
