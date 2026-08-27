import random
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.modules.patients.models import Patient
from app.modules.patients.schemas import PatientCreate, PatientUpdate, Patient360Summary
from app.modules.appointments.models import Appointment
from app.modules.opd.models import OPDVisit, VitalSigns
from app.modules.ipd.models import Admission
from app.modules.clinical.models import Prescription, Allergy
from app.core.exceptions import NotFoundError, ConflictError

class PatientService:
    @staticmethod
    def generate_uhid(db: Session) -> str:
        year = datetime.utcnow().year
        count = db.query(Patient).count() + 1
        return f"APX-{year}-{count:05d}"

    @staticmethod
    def get_by_id(db: Session, patient_id: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.id == patient_id).first()

    @staticmethod
    def get_by_uhid(db: Session, uhid: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.uhid == uhid).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 20, search: Optional[str] = None) -> Tuple[List[Patient], int]:
        query = db.query(Patient)
        if search:
            query = query.filter(
                (Patient.uhid.ilike(f"%{search}%")) |
                (Patient.first_name.ilike(f"%{search}%")) |
                (Patient.last_name.ilike(f"%{search}%")) |
                (Patient.phone_number.ilike(f"%{search}%")) |
                (Patient.email.ilike(f"%{search}%"))
            )
        total = query.count()
        patients = query.order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()
        return patients, total

    @staticmethod
    def create(db: Session, patient_in: PatientCreate, created_by: Optional[str] = None) -> Patient:
        uhid = PatientService.generate_uhid(db)
        patient = Patient(
            uhid=uhid,
            **patient_in.model_dump(),
            created_by=created_by
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def update(db: Session, patient_id: str, patient_in: PatientUpdate, updated_by: Optional[str] = None) -> Patient:
        patient = PatientService.get_by_id(db, patient_id)
        if not patient:
            raise NotFoundError("Patient not found")
        
        for key, val in patient_in.model_dump(exclude_unset=True).items():
            setattr(patient, key, val)
        
        patient.updated_by = updated_by
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def get_patient_360(db: Session, patient_id: str) -> Dict[str, Any]:
        patient = PatientService.get_by_id(db, patient_id)
        if not patient:
            raise NotFoundError("Patient not found")

        total_appts = db.query(Appointment).filter(Appointment.patient_id == patient_id).count()
        total_opd = db.query(OPDVisit).filter(OPDVisit.patient_id == patient_id).count()
        total_ipd = db.query(Admission).filter(Admission.patient_id == patient_id).count()
        active_rx = db.query(Prescription).filter(Prescription.patient_id == patient_id).count()
        
        latest_vital = db.query(VitalSigns).filter(VitalSigns.patient_id == patient_id).order_by(VitalSigns.recorded_at.desc()).first()
        allergies = db.query(Allergy).filter(Allergy.patient_id == patient_id).all()

        vitals_dict = None
        if latest_vital:
            vitals_dict = {
                "bp": f"{latest_vital.systolic_bp}/{latest_vital.diastolic_bp}" if latest_vital.systolic_bp else "N/A",
                "pulse": latest_vital.pulse_rate,
                "temp": latest_vital.temperature_celsius,
                "spo2": latest_vital.spo2_percentage,
                "recorded_at": latest_vital.recorded_at
            }

        return {
            "patient": patient,
            "total_appointments": total_appts,
            "total_opd_visits": total_opd,
            "total_admissions": total_ipd,
            "active_prescriptions_count": active_rx,
            "recent_vitals": vitals_dict,
            "recent_allergies": [f"{a.allergen_name} ({a.severity})" for a in allergies]
        }
