from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.users.schemas import UserResponse

class DoctorScheduleBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    max_patients: int = 30
    is_active_day: bool = True

class DoctorScheduleCreate(DoctorScheduleBase):
    pass

class DoctorScheduleResponse(DoctorScheduleBase):
    id: str

    class Config:
        from_attributes = True

class DoctorBase(BaseModel):
    license_number: str
    specialization: str
    sub_specialties: Optional[str] = None
    qualification: str
    experience_years: int = 0
    department_id: Optional[str] = None
    consultation_room: Optional[str] = None
    consultation_fee: float = 100.0
    follow_up_fee: float = 50.0
    follow_up_validity_days: int = 7
    slot_duration_minutes: int = 15
    bio: Optional[str] = None
    is_available_for_teleconsult: bool = False
    is_on_duty: bool = True

class DoctorCreate(DoctorBase):
    user_id: str
    doctor_code: Optional[str] = None
    schedules: Optional[List[DoctorScheduleCreate]] = []

class DoctorUpdate(BaseModel):
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    consultation_fee: Optional[float] = None
    consultation_room: Optional[str] = None
    is_on_duty: Optional[bool] = None

class DoctorResponse(DoctorBase):
    id: str
    doctor_code: str
    user: Optional[UserResponse] = None
    schedules: List[DoctorScheduleResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
