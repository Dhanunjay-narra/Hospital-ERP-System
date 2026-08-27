from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.hr.models import Employee, StaffLeaveRequest
from app.modules.hr.schemas import EmployeeCreate, StaffLeaveCreate
from app.core.exceptions import NotFoundError, ConflictError

class HRService:
    @staticmethod
    def get_employees(db: Session, skip: int = 0, limit: int = 20, department_id: Optional[str] = None) -> Tuple[List[Employee], int]:
        query = db.query(Employee)
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        total = query.count()
        employees = query.offset(skip).limit(limit).all()
        return employees, total

    @staticmethod
    def create_employee(db: Session, emp_in: EmployeeCreate, created_by: Optional[str] = None) -> Employee:
        existing = db.query(Employee).filter(Employee.user_id == emp_in.user_id).first()
        if existing:
            return existing
        count = db.query(Employee).count() + 1
        emp = Employee(
            employee_code=f"EMP-{datetime.utcnow().year}-{count:04d}",
            status="ACTIVE",
            **emp_in.model_dump(),
            created_by=created_by
        )
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return emp

    @staticmethod
    def get_leaves(db: Session) -> List[StaffLeaveRequest]:
        return db.query(StaffLeaveRequest).order_by(StaffLeaveRequest.created_at.desc()).all()

    @staticmethod
    def request_leave(db: Session, leave_in: StaffLeaveCreate, created_by: Optional[str] = None) -> StaffLeaveRequest:
        leave = StaffLeaveRequest(
            status="PENDING",
            **leave_in.model_dump(),
            created_by=created_by
        )
        db.add(leave)
        db.commit()
        db.refresh(leave)
        return leave
