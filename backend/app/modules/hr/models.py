import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Employee(BaseModel):
    __tablename__ = "employees"

    employee_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. EMP-2026-001
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    
    designation = Column(String(100), nullable=False) # Senior Resident, Head Nurse, Pharmacist, Billing Executive
    employment_type = Column(String(50), default="FULL_TIME", nullable=False) # FULL_TIME, PART_TIME, CONTRACT, CONSULTANT
    joining_date = Column(Date, nullable=False)
    salary_amount = Column(Float, default=5000.0, nullable=False)
    bank_account_number = Column(String(50), nullable=True)
    emergency_contact = Column(String(100), nullable=True)
    
    # STATUS: ACTIVE, ON_LEAVE, PROBATION, TERMINATED, RESIGNED
    status = Column(String(30), default="ACTIVE", index=True, nullable=False)

    user = relationship("User", lazy="joined")
    department = relationship("Department", lazy="joined")

class StaffLeaveRequest(BaseModel):
    __tablename__ = "staff_leave_requests"

    employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    leave_type = Column(String(50), default="CASUAL", nullable=False) # CASUAL, SICK, ANNUAL, MATERNITY
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    
    # STATUS: PENDING, APPROVED, REJECTED
    status = Column(String(30), default="PENDING", index=True, nullable=False)
    approved_by_id = Column(String(36), nullable=True)

    employee = relationship("Employee", lazy="joined")
