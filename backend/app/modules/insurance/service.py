from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.insurance.models import InsuranceProvider, InsuranceClaim
from app.modules.insurance.schemas import InsuranceProviderCreate, InsuranceClaimCreate
from app.core.exceptions import NotFoundError, ConflictError

class InsuranceService:
    @staticmethod
    def get_providers(db: Session) -> List[InsuranceProvider]:
        return db.query(InsuranceProvider).all()

    @staticmethod
    def create_provider(db: Session, prov_in: InsuranceProviderCreate) -> InsuranceProvider:
        prov = InsuranceProvider(**prov_in.model_dump())
        db.add(prov)
        db.commit()
        db.refresh(prov)
        return prov

    @staticmethod
    def get_claims(db: Session, skip: int = 0, limit: int = 20, patient_id: Optional[str] = None, status: Optional[str] = None) -> Tuple[List[InsuranceClaim], int]:
        query = db.query(InsuranceClaim)
        if patient_id:
            query = query.filter(InsuranceClaim.patient_id == patient_id)
        if status:
            query = query.filter(InsuranceClaim.status == status)
        total = query.count()
        claims = query.order_by(InsuranceClaim.submission_date.desc()).offset(skip).limit(limit).all()
        return claims, total

    @staticmethod
    def submit_claim(db: Session, claim_in: InsuranceClaimCreate, created_by: Optional[str] = None) -> InsuranceClaim:
        count = db.query(InsuranceClaim).count() + 1
        claim = InsuranceClaim(
            claim_number=f"CLM-{datetime.utcnow().year}-{count:05d}",
            status="SUBMITTED",
            approved_amount=claim_in.total_claim_amount * 0.85, # Default pre-estimate
            patient_copay_amount=claim_in.total_claim_amount * 0.15,
            deduction_amount=0.0,
            **claim_in.model_dump(),
            created_by=created_by
        )
        db.add(claim)
        db.commit()
        db.refresh(claim)
        return claim
