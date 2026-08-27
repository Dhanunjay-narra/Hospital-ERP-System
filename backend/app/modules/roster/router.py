from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.hr.models import Employee
from app.modules.roster.schemas import (
    RosterSlotCreate, RosterSlotResponse,
    ShiftHandoverCreate, ShiftHandoverResponse
)
from app.modules.roster.service import RosterService

router = APIRouter(prefix="/roster", tags=["Duty Roster & Shift Handover"])

@router.get("/slots", response_model=List[RosterSlotResponse])
def list_roster_slots(
    department_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RosterService.get_slots(db, department_id=department_id)

@router.post("/slots", response_model=RosterSlotResponse)
def create_roster_slot(
    slot_in: RosterSlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "NURSING_SUPERVISOR", "HR_MANAGER"))
):
    return RosterService.create_slot(db, slot_in, created_by=current_user.id)

@router.get("/handovers", response_model=List[ShiftHandoverResponse])
def list_shift_handovers(
    department_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return RosterService.get_handovers(db, department_id=department_id)

@router.post("/handovers", response_model=ShiftHandoverResponse)
def submit_shift_handover(
    ho_in: ShiftHandoverCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find employee profile of current user
    emp = db.query(Employee).filter(Employee.user_id == current_user.id).first()
    outgoing_id = emp.id if emp else current_user.id
    return RosterService.create_handover(db, ho_in, outgoing_employee_id=outgoing_id)
