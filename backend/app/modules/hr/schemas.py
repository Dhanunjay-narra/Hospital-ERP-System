from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel
from app.modules.users.schemas import UserResponse
from app.modules.organization.schemas import DepartmentResponse

class EmployeeBase(BaseModel):
    user_id: str
    department_id: Optional[str] = None
    designation: str
    employment_type: str = "FULL_TIME"
    joining_date: date
    salary_amount: float = 5000.0
    bank_account_number: Optional[str] = None
    emergency_contact: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: str
    employee_code: str
    status: str
    user: Optional[UserResponse] = None
    department: Optional[DepartmentResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StaffLeaveCreate(BaseModel):
    employee_id: str
    leave_type: str = "CASUAL"
    start_date: date
    end_date: date
    reason: str

class StaffLeaveResponse(StaffLeaveCreate):
    id: str
    status: str
    employee: Optional[EmployeeResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
