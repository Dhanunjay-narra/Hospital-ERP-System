from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from app.modules.hr.schemas import EmployeeResponse
from app.modules.organization.schemas import DepartmentResponse

class RosterSlotBase(BaseModel):
    department_id: str
    employee_id: str
    shift_date: date
    shift_type: str = "MORNING" # MORNING, EVENING, NIGHT, ON_CALL
    start_time: str = "07:00"
    end_time: str = "15:00"
    assigned_role: str = "Primary On-Duty"
    is_present: bool = True

class RosterSlotCreate(RosterSlotBase):
    pass

class RosterSlotResponse(RosterSlotBase):
    id: str
    department: Optional[DepartmentResponse] = None
    employee: Optional[EmployeeResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ShiftHandoverCreate(BaseModel):
    department_id: str
    incoming_employee_id: str
    shift_date: date
    critical_patient_notes: str
    pending_tasks: Optional[str] = None
    narcotics_count_verified: bool = True

class ShiftHandoverResponse(ShiftHandoverCreate):
    id: str
    outgoing_employee_id: str
    handover_time: datetime
    department: Optional[DepartmentResponse] = None
    outgoing_employee: Optional[EmployeeResponse] = None
    incoming_employee: Optional[EmployeeResponse] = None

    class Config:
        from_attributes = True
