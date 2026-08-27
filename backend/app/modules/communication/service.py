from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.communication.models import CommunicationTemplate, DispatchedMessage
from app.modules.communication.schemas import CommunicationTemplateCreate, DispatchedMessageCreate
from app.core.exceptions import NotFoundError

class CommunicationService:
    @staticmethod
    def get_templates(db: Session) -> List[CommunicationTemplate]:
        return db.query(CommunicationTemplate).all()

    @staticmethod
    def create_template(db: Session, tpl_in: CommunicationTemplateCreate) -> CommunicationTemplate:
        existing = db.query(CommunicationTemplate).filter(CommunicationTemplate.template_code == tpl_in.template_code).first()
        if existing:
            return existing
        tpl = CommunicationTemplate(**tpl_in.model_dump())
        db.add(tpl)
        db.commit()
        db.refresh(tpl)
        return tpl

    @staticmethod
    def get_messages(db: Session, skip: int = 0, limit: int = 20) -> Tuple[List[DispatchedMessage], int]:
        total = db.query(DispatchedMessage).count()
        msgs = db.query(DispatchedMessage).order_by(DispatchedMessage.sent_at.desc()).offset(skip).limit(limit).all()
        return msgs, total

    @staticmethod
    def dispatch_message(db: Session, msg_in: DispatchedMessageCreate, created_by: Optional[str] = None) -> DispatchedMessage:
        msg = DispatchedMessage(
            status="SENT",
            **msg_in.model_dump(),
            created_by=created_by
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg
