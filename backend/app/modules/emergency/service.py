from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.emergency.models import EmergencyTriage
from app.modules.emergency.schemas import EmergencyTriageCreate
from app.core.exceptions import NotFoundError
from app.core.events import event_bus

class EmergencyService:
    @staticmethod
    def get_all_triages(db: Session, skip: int = 0, limit: int = 20, priority: Optional[str] = None, status: Optional[str] = None) -> Tuple[List[EmergencyTriage], int]:
        query = db.query(EmergencyTriage)
        if priority:
            query = query.filter(EmergencyTriage.priority_level == priority)
        if status:
            query = query.filter(EmergencyTriage.status == status)
        total = query.count()
        triages = query.order_by(EmergencyTriage.created_at.desc()).offset(skip).limit(limit).all()
        return triages, total

    @staticmethod
    def create_triage(db: Session, triage_in: EmergencyTriageCreate, created_by: Optional[str] = None) -> EmergencyTriage:
        count = db.query(EmergencyTriage).count() + 1
        triage = EmergencyTriage(
            triage_number=f"ER-{datetime.utcnow().year}-{count:05d}",
            status="TRIAGED",
            **triage_in.model_dump(),
            created_by=created_by
        )
        db.add(triage)
        db.commit()
        db.refresh(triage)

        event_bus.publish("emergency.patient_triaged", {
            "triage_id": triage.id,
            "patient_id": triage.patient_id,
            "priority": triage.priority_level
        })

        return triage
