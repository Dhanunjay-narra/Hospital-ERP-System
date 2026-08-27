from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.crm.models import PatientLead, LeadInteraction
from app.modules.crm.schemas import PatientLeadCreate, LeadInteractionCreate
from app.core.exceptions import NotFoundError

class CRMService:
    @staticmethod
    def get_leads(db: Session, skip: int = 0, limit: int = 20, status: Optional[str] = None) -> Tuple[List[PatientLead], int]:
        query = db.query(PatientLead)
        if status:
            query = query.filter(PatientLead.status == status)
        total = query.count()
        leads = query.order_by(PatientLead.created_at.desc()).offset(skip).limit(limit).all()
        return leads, total

    @staticmethod
    def create_lead(db: Session, lead_in: PatientLeadCreate, created_by: Optional[str] = None) -> PatientLead:
        count = db.query(PatientLead).count() + 1
        lead = PatientLead(
            lead_code=f"LEAD-{datetime.utcnow().year}-{count:05d}",
            status="NEW",
            **lead_in.model_dump(),
            created_by=created_by
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return lead

    @staticmethod
    def add_interaction(db: Session, lead_id: str, inter_in: LeadInteractionCreate, user_id: Optional[str] = None) -> LeadInteraction:
        lead = db.query(PatientLead).filter(PatientLead.id == lead_id).first()
        if not lead:
            raise NotFoundError("Lead not found")

        interaction = LeadInteraction(
            lead_id=lead_id,
            counselor_user_id=user_id,
            **inter_in.model_dump()
        )
        db.add(interaction)
        lead.status = "CONTACTED"
        db.commit()
        db.refresh(interaction)
        return interaction
