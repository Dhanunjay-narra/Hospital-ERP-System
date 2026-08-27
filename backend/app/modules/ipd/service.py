from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.ipd.models import Admission, DailyClinicalRound
from app.modules.ipd.schemas import AdmissionCreate, DischargeRequest, DailyClinicalRoundCreate
from app.modules.organization.models import Bed
from app.core.exceptions import NotFoundError, ConflictError
from app.core.events import event_bus

class IPDService:
    @staticmethod
    def get_all_admissions(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        ward_id: Optional[str] = None,
        doctor_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Admission], int]:
        query = db.query(Admission)
        if ward_id:
            query = query.filter(Admission.ward_id == ward_id)
        if doctor_id:
            query = query.filter(Admission.primary_doctor_id == doctor_id)
        if status:
            query = query.filter(Admission.status == status)

        total = query.count()
        admissions = query.order_by(Admission.admission_date.desc()).offset(skip).limit(limit).all()
        return admissions, total

    @staticmethod
    def get_admission_by_id(db: Session, admission_id: str) -> Optional[Admission]:
        return db.query(Admission).filter(Admission.id == admission_id).first()

    @staticmethod
    def admit_patient(db: Session, adm_in: AdmissionCreate, created_by: Optional[str] = None) -> Admission:
        count = db.query(Admission).count() + 1
        admission = Admission(
            admission_number=f"IPD-{datetime.utcnow().year}-{count:05d}",
            status="ADMITTED",
            **adm_in.model_dump(),
            created_by=created_by
        )
        db.add(admission)
        db.flush()

        # Update bed status to OCCUPIED
        if adm_in.bed_id:
            bed = db.query(Bed).filter(Bed.id == adm_in.bed_id).first()
            if bed:
                bed.status = "OCCUPIED"
                bed.current_patient_id = adm_in.patient_id
                bed.current_admission_id = admission.id

        db.commit()
        db.refresh(admission)

        event_bus.publish("ipd.patient_admitted", {
            "admission_id": admission.id,
            "patient_id": admission.patient_id,
            "bed_id": admission.bed_id
        })

        return admission

    @staticmethod
    def discharge_patient(db: Session, admission_id: str, dis_in: DischargeRequest) -> Admission:
        adm = IPDService.get_admission_by_id(db, admission_id)
        if not adm:
            raise NotFoundError("Admission record not found")

        adm.status = "DISCHARGED"
        adm.discharge_date = datetime.utcnow()
        adm.discharge_type = dis_in.discharge_type
        adm.discharge_diagnosis = dis_in.discharge_diagnosis
        adm.discharge_summary = dis_in.discharge_summary
        adm.discharge_instructions = dis_in.discharge_instructions

        # Free bed
        if adm.bed_id:
            bed = db.query(Bed).filter(Bed.id == adm.bed_id).first()
            if bed:
                bed.status = "CLEANING"
                bed.current_patient_id = None
                bed.current_admission_id = None

        db.commit()
        db.refresh(adm)

        event_bus.publish("ipd.patient_discharged", {
            "admission_id": adm.id,
            "patient_id": adm.patient_id
        })

        return adm

    @staticmethod
    def add_daily_round(db: Session, round_in: DailyClinicalRoundCreate, doctor_id: str) -> DailyClinicalRound:
        clinical_round = DailyClinicalRound(
            admission_id=round_in.admission_id,
            doctor_id=doctor_id,
            clinical_observations=round_in.clinical_observations,
            treatment_orders=round_in.treatment_orders,
            nursing_instructions=round_in.nursing_instructions,
            dietary_orders=round_in.dietary_orders
        )
        db.add(clinical_round)
        db.commit()
        db.refresh(clinical_round)
        return clinical_round
