from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.opd.models import OPDVisit, VitalSigns
from app.modules.opd.schemas import OPDVisitCreate, OPDConsultationUpdate, VitalSignsCreate
from app.core.exceptions import NotFoundError

class OPDService:
    @staticmethod
    def get_all_visits(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        doctor_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[OPDVisit], int]:
        query = db.query(OPDVisit)
        if doctor_id:
            query = query.filter(OPDVisit.doctor_id == doctor_id)
        if status:
            query = query.filter(OPDVisit.status == status)

        total = query.count()
        visits = query.order_by(OPDVisit.visit_datetime.desc()).offset(skip).limit(limit).all()
        return visits, total

    @staticmethod
    def get_visit_by_id(db: Session, visit_id: str) -> Optional[OPDVisit]:
        return db.query(OPDVisit).filter(OPDVisit.id == visit_id).first()

    @staticmethod
    def create_visit(db: Session, visit_in: OPDVisitCreate, created_by: Optional[str] = None) -> OPDVisit:
        count = db.query(OPDVisit).count() + 1
        day_token = db.query(OPDVisit).filter(OPDVisit.doctor_id == visit_in.doctor_id).count() + 1
        
        visit = OPDVisit(
            visit_number=f"OPD-{datetime.utcnow().year}-{count:05d}",
            queue_number=day_token,
            **visit_in.model_dump(),
            created_by=created_by
        )
        db.add(visit)
        db.commit()
        db.refresh(visit)
        return visit

    @staticmethod
    def record_consultation(db: Session, visit_id: str, consult_in: OPDConsultationUpdate) -> OPDVisit:
        visit = OPDService.get_visit_by_id(db, visit_id)
        if not visit:
            raise NotFoundError("OPD Visit not found")

        for key, val in consult_in.model_dump(exclude_unset=True).items():
            setattr(visit, key, val)

        db.commit()
        db.refresh(visit)
        return visit

    @staticmethod
    def record_vitals(db: Session, vitals_in: VitalSignsCreate, recorded_by: Optional[str] = None) -> VitalSigns:
        bmi = None
        if vitals_in.height_cm and vitals_in.weight_kg and vitals_in.height_cm > 0:
            height_m = vitals_in.height_cm / 100.0
            bmi = round(vitals_in.weight_kg / (height_m * height_m), 1)

        vitals = VitalSigns(
            bmi=bmi,
            recorded_by=recorded_by,
            **vitals_in.model_dump()
        )
        db.add(vitals)
        db.commit()
        db.refresh(vitals)
        return vitals
