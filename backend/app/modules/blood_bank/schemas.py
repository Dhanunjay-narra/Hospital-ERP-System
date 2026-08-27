from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class BloodDonorCreate(BaseModel):
    full_name: str
    gender: str
    date_of_birth: date
    blood_group: str
    phone_number: str
    email: Optional[str] = None
    hemoglobin_level: float = 13.5

class BloodDonorResponse(BloodDonorCreate):
    id: str
    donor_code: str
    is_eligible: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BloodUnitCreate(BaseModel):
    donor_id: Optional[str] = None
    blood_group: str
    component_type: str = "PRBC" # WHOLE_BLOOD, PRBC, FFP, PLATELETS
    volume_ml: float = 350.0
    collection_date: date
    expiry_date: date
    storage_refrigerator_id: str = "REF-COLD-1 (4°C)"

class BloodUnitResponse(BloodUnitCreate):
    id: str
    unit_number: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
