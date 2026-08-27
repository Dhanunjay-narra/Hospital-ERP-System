from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.roster.models import RosterSlot, ShiftHandoverLog
from app.modules.roster.schemas import RosterSlotCreate, ShiftHandoverCreate
from app.core.exceptions import NotFoundError

class RosterService:
    @staticmethod
    def get_slots(db: Session, department_id: Optional[str] = None) -> List[RosterSlot]:
        query = db.query(RosterSlot)
        if department_id:
            query = query.filter(RosterSlot.department_id == department_id)
        return query.order_by(RosterSlot.shift_date.desc()).all()

    @staticmethod
    def create_slot(db: Session, slot_in: RosterSlotCreate, created_by: Optional[str] = None) -> RosterSlot:
        slot = RosterSlot(**slot_in.model_dump(), created_by=created_by)
        db.add(slot)
        db.commit()
        db.refresh(slot)
        return slot

    @staticmethod
    def get_handovers(db: Session, department_id: Optional[str] = None) -> List[ShiftHandoverLog]:
        query = db.query(ShiftHandoverLog)
        if department_id:
            query = query.filter(ShiftHandoverLog.department_id == department_id)
        return query.order_by(ShiftHandoverLog.handover_time.desc()).all()

    @staticmethod
    def create_handover(db: Session, ho_in: ShiftHandoverCreate, outgoing_employee_id: str) -> ShiftHandoverLog:
        ho = ShiftHandoverLog(
            outgoing_employee_id=outgoing_employee_id,
            **ho_in.model_dump()
        )
        db.add(ho)
        db.commit()
        db.refresh(ho)
        return ho
