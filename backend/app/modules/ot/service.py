from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.ot.models import OTRoom, SurgeryBooking
from app.modules.ot.schemas import OTRoomCreate, SurgeryBookingCreate
from app.core.exceptions import NotFoundError

class OTService:
    @staticmethod
    def get_rooms(db: Session) -> List[OTRoom]:
        return db.query(OTRoom).all()

    @staticmethod
    def create_room(db: Session, room_in: OTRoomCreate) -> OTRoom:
        room = OTRoom(**room_in.model_dump())
        db.add(room)
        db.commit()
        db.refresh(room)
        return room

    @staticmethod
    def get_surgeries(db: Session, skip: int = 0, limit: int = 20, ot_room_id: Optional[str] = None, status: Optional[str] = None) -> Tuple[List[SurgeryBooking], int]:
        query = db.query(SurgeryBooking)
        if ot_room_id:
            query = query.filter(SurgeryBooking.ot_room_id == ot_room_id)
        if status:
            query = query.filter(SurgeryBooking.status == status)
        total = query.count()
        surgeries = query.order_by(SurgeryBooking.scheduled_start.asc()).offset(skip).limit(limit).all()
        return surgeries, total

    @staticmethod
    def book_surgery(db: Session, surg_in: SurgeryBookingCreate, created_by: Optional[str] = None) -> SurgeryBooking:
        count = db.query(SurgeryBooking).count() + 1
        surg = SurgeryBooking(
            surgery_number=f"SURG-{datetime.utcnow().year}-{count:05d}",
            status="SCHEDULED",
            **surg_in.model_dump(),
            created_by=created_by
        )
        db.add(surg)
        db.commit()
        db.refresh(surg)
        return surg
