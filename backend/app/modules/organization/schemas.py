from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class BedBase(BaseModel):
    bed_number: str
    status: str = "AVAILABLE"
    bed_type: str = "STANDARD"
    room_id: Optional[str] = None
    ward_id: str

class BedCreate(BedBase):
    pass

class BedUpdate(BaseModel):
    bed_number: Optional[str] = None
    status: Optional[str] = None
    bed_type: Optional[str] = None
    room_id: Optional[str] = None
    current_patient_id: Optional[str] = None
    current_admission_id: Optional[str] = None

class BedResponse(BedBase):
    id: str
    current_patient_id: Optional[str] = None
    current_admission_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str
    room_type: str = "GENERAL"
    daily_rate: int = 0
    ward_id: Optional[str] = None
    floor_id: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: str
    beds: List[BedResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class WardBase(BaseModel):
    name: str
    code: str
    gender_type: str = "ALL"
    ward_type: str = "GENERAL"
    branch_id: str
    floor_id: Optional[str] = None
    department_id: Optional[str] = None

class WardCreate(WardBase):
    pass

class WardResponse(WardBase):
    id: str
    rooms: List[RoomResponse] = []
    beds: List[BedResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    code: str
    department_type: str = "CLINICAL"
    branch_id: str
    description: Optional[str] = None
    is_opd: bool = True
    is_ipd: bool = True
    is_emergency: bool = False

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class HospitalBranchBase(BaseModel):
    name: str
    code: str
    is_main_branch: bool = False
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class HospitalBranchCreate(HospitalBranchBase):
    organization_id: str

class HospitalBranchResponse(HospitalBranchBase):
    id: str
    organization_id: str
    departments: List[DepartmentResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

class OrganizationBase(BaseModel):
    name: str
    code: str
    registration_number: Optional[str] = None
    tax_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    currency: str = "USD"
    timezone: str = "UTC"

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: str
    branches: List[HospitalBranchResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
