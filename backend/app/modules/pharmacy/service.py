from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.pharmacy.models import MedicineMaster, MedicineBatch
from app.modules.pharmacy.schemas import MedicineCreate, MedicineBatchCreate
from app.core.exceptions import NotFoundError, ConflictError

class PharmacyService:
    @staticmethod
    def get_all_medicines(db: Session, skip: int = 0, limit: int = 20, search: Optional[str] = None, category: Optional[str] = None) -> Tuple[List[MedicineMaster], int]:
        query = db.query(MedicineMaster)
        if search:
            query = query.filter((MedicineMaster.name.ilike(f"%{search}%")) | (MedicineMaster.generic_name.ilike(f"%{search}%")))
        if category:
            query = query.filter(MedicineMaster.category == category)
        total = query.count()
        meds = query.offset(skip).limit(limit).all()
        return meds, total

    @staticmethod
    def create_medicine(db: Session, med_in: MedicineCreate, created_by: Optional[str] = None) -> MedicineMaster:
        existing = db.query(MedicineMaster).filter(MedicineMaster.sku_code == med_in.sku_code).first()
        if existing:
            raise ConflictError("Medicine with this SKU code already exists")

        med = MedicineMaster(
            name=med_in.name,
            generic_name=med_in.generic_name,
            sku_code=med_in.sku_code,
            category=med_in.category,
            dosage_form=med_in.dosage_form,
            strength=med_in.strength,
            manufacturer=med_in.manufacturer,
            unit_price=med_in.unit_price,
            mrp=med_in.mrp,
            reorder_level=med_in.reorder_level,
            created_by=created_by
        )
        db.add(med)
        db.flush()

        if med_in.batches:
            for b in med_in.batches:
                batch = MedicineBatch(
                    medicine_id=med.id,
                    batch_number=b.batch_number,
                    expiry_date=b.expiry_date,
                    manufacturing_date=b.manufacturing_date,
                    quantity_received=b.quantity_received,
                    quantity_available=b.quantity_received,
                    purchase_rate=b.purchase_rate,
                    selling_price=b.selling_price,
                    storage_location=b.storage_location
                )
                db.add(batch)

        db.commit()
        db.refresh(med)
        return med

    @staticmethod
    def add_batch(db: Session, medicine_id: str, batch_in: MedicineBatchCreate) -> MedicineBatch:
        med = db.query(MedicineMaster).filter(MedicineMaster.id == medicine_id).first()
        if not med:
            raise NotFoundError("Medicine not found")

        batch = MedicineBatch(
            medicine_id=medicine_id,
            quantity_available=batch_in.quantity_received,
            **batch_in.model_dump()
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch
