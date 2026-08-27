from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.nursing.models import MedicationAdministrationRecord, NursingNote, IntakeOutputChart
from app.modules.nursing.schemas import MARCreate, MARAdministerRequest, NursingNoteCreate, IntakeOutputChartCreate
from app.core.exceptions import NotFoundError

class NursingService:
    @staticmethod
    def get_mar_records(db: Session, admission_id: str) -> List[MedicationAdministrationRecord]:
        return db.query(MedicationAdministrationRecord).filter(
            MedicationAdministrationRecord.admission_id == admission_id
        ).order_by(MedicationAdministrationRecord.scheduled_time.asc()).all()

    @staticmethod
    def schedule_mar_dose(db: Session, mar_in: MARCreate) -> MedicationAdministrationRecord:
        mar = MedicationAdministrationRecord(**mar_in.model_dump())
        db.add(mar)
        db.commit()
        db.refresh(mar)
        return mar

    @staticmethod
    def record_dose_administered(db: Session, mar_id: str, admin_req: MARAdministerRequest, nurse_id: str) -> MedicationAdministrationRecord:
        mar = db.query(MedicationAdministrationRecord).filter(MedicationAdministrationRecord.id == mar_id).first()
        if not mar:
            raise NotFoundError("MAR record not found")

        mar.status = admin_req.status
        mar.administered_time = datetime.utcnow()
        mar.administered_by_nurse_id = nurse_id
        mar.notes = admin_req.notes

        db.commit()
        db.refresh(mar)
        return mar

    @staticmethod
    def add_nursing_note(db: Session, note_in: NursingNoteCreate, nurse_id: str) -> NursingNote:
        note = NursingNote(nurse_id=nurse_id, **note_in.model_dump())
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def get_nursing_notes(db: Session, admission_id: str) -> List[NursingNote]:
        return db.query(NursingNote).filter(NursingNote.admission_id == admission_id).order_by(NursingNote.note_datetime.desc()).all()

    @staticmethod
    def record_intake_output(db: Session, io_in: IntakeOutputChartCreate, recorded_by: Optional[str] = None) -> IntakeOutputChart:
        total_in = io_in.oral_intake_ml + io_in.iv_fluids_ml + io_in.ng_tube_ml
        total_out = io_in.urine_output_ml + io_in.drain_output_ml + io_in.vomitus_ml
        balance = total_in - total_out

        io_record = IntakeOutputChart(
            total_intake_ml=total_in,
            total_output_ml=total_out,
            balance_ml=balance,
            recorded_by=recorded_by,
            **io_in.model_dump()
        )
        db.add(io_record)
        db.commit()
        db.refresh(io_record)
        return io_record

    @staticmethod
    def get_io_charts(db: Session, admission_id: str) -> List[IntakeOutputChart]:
        return db.query(IntakeOutputChart).filter(IntakeOutputChart.admission_id == admission_id).order_by(IntakeOutputChart.recorded_at.desc()).all()
