from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.telemedicine.models import TeleconsultationSession
from app.modules.telemedicine.schemas import TeleconsultationCreate
from app.core.exceptions import NotFoundError

class TelemedicineService:
    @staticmethod
    def get_sessions(db: Session, skip: int = 0, limit: int = 20) -> Tuple[List[TeleconsultationSession], int]:
        total = db.query(TeleconsultationSession).count()
        sessions = db.query(TeleconsultationSession).order_by(TeleconsultationSession.scheduled_start.desc()).offset(skip).limit(limit).all()
        return sessions, total

    @staticmethod
    def create_session(db: Session, ses_in: TeleconsultationCreate, created_by: Optional[str] = None) -> TeleconsultationSession:
        count = db.query(TeleconsultationSession).count() + 1
        code = f"VIRT-{datetime.utcnow().year}-{count:05d}"
        session = TeleconsultationSession(
            session_code=code,
            meeting_room_url=f"https://telehealth.apexhealth.org/room/{code}",
            status="SCHEDULED",
            **ses_in.model_dump(),
            created_by=created_by
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
