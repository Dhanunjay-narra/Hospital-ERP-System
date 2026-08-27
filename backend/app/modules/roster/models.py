import uuid
from datetime import datetime, date, time
from sqlalchemy import Column, String, Boolean, DateTime, Date, Time, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class RosterSlot(BaseModel):
    __tablename__ = "roster_slots"

    department_id = Column(String(36), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    
    shift_date = Column(Date, index=True, nullable=False)
    # SHIFT_TYPE: MORNING (07:00-15:00), EVENING (15:00-23:00), NIGHT (23:00-07:00), ON_CALL (24 Hours)
    shift_type = Column(String(30), default="MORNING", nullable=False)
    start_time = Column(String(10), default="07:00", nullable=False)
    end_time = Column(String(10), default="15:00", nullable=False)
    
    assigned_role = Column(String(100), default="Primary On-Duty", nullable=False)
    is_present = Column(Boolean, default=True, nullable=False)

    department = relationship("Department", lazy="joined")
    employee = relationship("Employee", lazy="joined")

class ShiftHandoverLog(BaseModel):
    __tablename__ = "shift_handover_logs"

    department_id = Column(String(36), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    outgoing_employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    incoming_employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    
    shift_date = Column(Date, nullable=False)
    critical_patient_notes = Column(Text, nullable=False)
    pending_tasks = Column(Text, nullable=True)
    narcotics_count_verified = Column(Boolean, default=True, nullable=False)
    handover_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    department = relationship("Department", lazy="joined")
    outgoing_employee = relationship("Employee", foreign_keys=[outgoing_employee_id], lazy="joined")
    incoming_employee = relationship("Employee", foreign_keys=[incoming_employee_id], lazy="joined")
