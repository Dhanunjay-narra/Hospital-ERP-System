from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.compliance.models import DataPrivacyConsent, SecurityEventLog
from app.modules.compliance.schemas import DataPrivacyConsentCreate, SecurityEventLogCreate
from app.core.exceptions import NotFoundError

class ComplianceService:
    @staticmethod
    def get_privacy_consents(db: Session, patient_id: Optional[str] = None) -> List[DataPrivacyConsent]:
        query = db.query(DataPrivacyConsent)
        if patient_id:
            query = query.filter(DataPrivacyConsent.patient_id == patient_id)
        return query.order_by(DataPrivacyConsent.consent_timestamp.desc()).all()

    @staticmethod
    def record_privacy_consent(db: Session, con_in: DataPrivacyConsentCreate) -> DataPrivacyConsent:
        con = DataPrivacyConsent(**con_in.model_dump())
        db.add(con)
        db.commit()
        db.refresh(con)
        return con

    @staticmethod
    def get_security_events(db: Session, skip: int = 0, limit: int = 20) -> Tuple[List[SecurityEventLog], int]:
        total = db.query(SecurityEventLog).count()
        events = db.query(SecurityEventLog).order_by(SecurityEventLog.timestamp.desc()).offset(skip).limit(limit).all()
        return events, total

    @staticmethod
    def log_security_event(db: Session, ev_in: SecurityEventLogCreate, actor_user_id: Optional[str] = None) -> SecurityEventLog:
        ev = SecurityEventLog(
            actor_user_id=actor_user_id,
            **ev_in.model_dump()
        )
        db.add(ev)
        db.commit()
        db.refresh(ev)
        return ev
