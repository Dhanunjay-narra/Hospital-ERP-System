from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.blood_bank.models import BloodDonor, BloodUnit
from app.modules.blood_bank.schemas import BloodDonorCreate, BloodUnitCreate
from app.core.exceptions import NotFoundError

class BloodBankService:
    @staticmethod
    def get_donors(db: Session) -> List[BloodDonor]:
        return db.query(BloodDonor).all()

    @staticmethod
    def register_donor(db: Session, donor_in: BloodDonorCreate, created_by: Optional[str] = None) -> BloodDonor:
        count = db.query(BloodDonor).count() + 1
        donor = BloodDonor(
            donor_code=f"DONOR-{datetime.utcnow().year}-{count:04d}",
            **donor_in.model_dump(),
            created_by=created_by
        )
        db.add(donor)
        db.commit()
        db.refresh(donor)
        return donor

    @staticmethod
    def get_units(db: Session, blood_group: Optional[str] = None, status: Optional[str] = None) -> List[BloodUnit]:
        query = db.query(BloodUnit)
        if blood_group:
            query = query.filter(BloodUnit.blood_group == blood_group)
        if status:
            query = query.filter(BloodUnit.status == status)
        return query.order_by(BloodUnit.expiry_date.asc()).all()

    @staticmethod
    def add_unit(db: Session, unit_in: BloodUnitCreate, created_by: Optional[str] = None) -> BloodUnit:
        count = db.query(BloodUnit).count() + 1
        unit = BloodUnit(
            unit_number=f"UNIT-{unit_in.blood_group.replace('+', 'POS').replace('-', 'NEG')}-{count:05d}",
            status="AVAILABLE",
            **unit_in.model_dump(),
            created_by=created_by
        )
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit
