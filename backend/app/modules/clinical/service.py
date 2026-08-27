from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.clinical.models import Prescription, PrescriptionItem, Allergy
from app.modules.clinical.schemas import PrescriptionCreate, AllergyCreate
from app.core.exceptions import NotFoundError
from app.core.events import event_bus

class ClinicalService:
    @staticmethod
    def get_prescriptions(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        patient_id: Optional[str] = None,
        doctor_id: Optional[str] = None
    ) -> Tuple[List[Prescription], int]:
        query = db.query(Prescription)
        if patient_id:
            query = query.filter(Prescription.patient_id == patient_id)
        if doctor_id:
            query = query.filter(Prescription.doctor_id == doctor_id)

        total = query.count()
        prescriptions = query.order_by(Prescription.issued_date.desc()).offset(skip).limit(limit).all()
        return prescriptions, total

    @staticmethod
    def create_prescription(db: Session, rx_in: PrescriptionCreate, created_by: Optional[str] = None) -> Prescription:
        count = db.query(Prescription).count() + 1
        rx_num = f"RX-{datetime.utcnow().year}-{count:05d}"

        rx = Prescription(
            prescription_number=rx_num,
            patient_id=rx_in.patient_id,
            doctor_id=rx_in.doctor_id,
            opd_visit_id=rx_in.opd_visit_id,
            admission_id=rx_in.admission_id,
            diagnosis_notes=rx_in.diagnosis_notes,
            general_advice=rx_in.general_advice,
            status="PENDING_DISPENSE",
            created_by=created_by
        )
        db.add(rx)
        db.flush()

        for item_in in rx_in.items:
            item = PrescriptionItem(
                prescription_id=rx.id,
                medicine_name=item_in.medicine_name,
                generic_name=item_in.generic_name,
                dosage=item_in.dosage,
                frequency=item_in.frequency,
                duration_days=item_in.duration_days,
                route=item_in.route,
                timing_instructions=item_in.timing_instructions,
                total_quantity=item_in.total_quantity
            )
            db.add(item)

        db.commit()
        db.refresh(rx)

        event_bus.publish("clinical.prescription_issued", {
            "prescription_id": rx.id,
            "patient_id": rx.patient_id,
            "doctor_id": rx.doctor_id
        })

        return rx

    @staticmethod
    def add_allergy(db: Session, allergy_in: AllergyCreate) -> Allergy:
        allergy = Allergy(**allergy_in.model_dump())
        db.add(allergy)
        db.commit()
        db.refresh(allergy)
        return allergy

    @staticmethod
    def get_patient_allergies(db: Session, patient_id: str) -> List[Allergy]:
        return db.query(Allergy).filter(Allergy.patient_id == patient_id).all()
