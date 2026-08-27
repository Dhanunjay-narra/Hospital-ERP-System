from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.medical_records.models import MedicalRecordArchive, RecordAccessLog
from app.modules.medical_records.schemas import MedicalRecordArchiveCreate, RecordAccessLogCreate
from app.core.exceptions import NotFoundError

class MedicalRecordService:
    @staticmethod
    def get_archives(db: Session, skip: int = 0, limit: int = 20, patient_id: Optional[str] = None) -> Tuple[List[MedicalRecordArchive], int]:
        query = db.query(MedicalRecordArchive)
        if patient_id:
            query = query.filter(MedicalRecordArchive.patient_id == patient_id)
        total = query.count()
        archives = query.order_by(MedicalRecordArchive.archived_date.desc()).offset(skip).limit(limit).all()
        return archives, total

    @staticmethod
    def archive_record(db: Session, arc_in: MedicalRecordArchiveCreate, created_by: Optional[str] = None) -> MedicalRecordArchive:
        count = db.query(MedicalRecordArchive).count() + 1
        arc = MedicalRecordArchive(
            archive_code=f"MRD-{datetime.utcnow().year}-{count:05d}",
            status="ARCHIVED",
            **arc_in.model_dump(),
            created_by=created_by
        )
        db.add(arc)
        db.commit()
        db.refresh(arc)
        return arc

    @staticmethod
    def log_access(db: Session, log_in: RecordAccessLogCreate, user_id: str) -> RecordAccessLog:
        log = RecordAccessLog(
            archive_id=log_in.archive_id,
            purpose=log_in.purpose,
            accessed_by_user_id=user_id
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
