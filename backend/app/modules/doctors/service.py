from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.doctors.models import Doctor, DoctorSchedule
from app.modules.doctors.schemas import DoctorCreate, DoctorUpdate
from app.modules.users.models import User
from app.core.exceptions import NotFoundError, ConflictError

class DoctorService:
    @staticmethod
    def get_by_id(db: Session, doctor_id: str) -> Optional[Doctor]:
        return db.query(Doctor).filter(Doctor.id == doctor_id).first()

    @staticmethod
    def get_by_user_id(db: Session, user_id: str) -> Optional[Doctor]:
        return db.query(Doctor).filter(Doctor.user_id == user_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 20, specialization: Optional[str] = None, department_id: Optional[str] = None) -> Tuple[List[Doctor], int]:
        query = db.query(Doctor)
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
        if department_id:
            query = query.filter(Doctor.department_id == department_id)
        total = query.count()
        doctors = query.offset(skip).limit(limit).all()
        return doctors, total

    @staticmethod
    def create(db: Session, doc_in: DoctorCreate, created_by: Optional[str] = None) -> Doctor:
        count = db.query(Doctor).count() + 101
        doc_code = doc_in.doctor_code or f"DOC-{count}"

        doctor = Doctor(
            doctor_code=doc_code,
            user_id=doc_in.user_id,
            license_number=doc_in.license_number,
            specialization=doc_in.specialization,
            sub_specialties=doc_in.sub_specialties,
            qualification=doc_in.qualification,
            experience_years=doc_in.experience_years,
            department_id=doc_in.department_id,
            consultation_room=doc_in.consultation_room,
            consultation_fee=doc_in.consultation_fee,
            follow_up_fee=doc_in.follow_up_fee,
            bio=doc_in.bio,
            created_by=created_by
        )
        db.add(doctor)
        db.flush()

        if doc_in.schedules:
            for s in doc_in.schedules:
                sched = DoctorSchedule(
                    doctor_id=doctor.id,
                    day_of_week=s.day_of_week,
                    start_time=s.start_time,
                    end_time=s.end_time,
                    max_patients=s.max_patients,
                    is_active_day=s.is_active_day
                )
                db.add(sched)

        db.commit()
        db.refresh(doctor)
        return doctor

    @staticmethod
    def update(db: Session, doctor_id: str, doc_in: DoctorUpdate) -> Doctor:
        doctor = DoctorService.get_by_id(db, doctor_id)
        if not doctor:
            raise NotFoundError("Doctor not found")
        for key, val in doc_in.model_dump(exclude_unset=True).items():
            setattr(doctor, key, val)
        db.commit()
        db.refresh(doctor)
        return doctor
