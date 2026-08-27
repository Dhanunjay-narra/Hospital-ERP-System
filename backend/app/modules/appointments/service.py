from datetime import datetime, date
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.appointments.models import Appointment
from app.modules.appointments.schemas import AppointmentCreate, AppointmentStatusUpdate
from app.modules.opd.models import OPDVisit
from app.core.exceptions import NotFoundError, ConflictError
from app.core.events import event_bus

class AppointmentService:
    @staticmethod
    def generate_appointment_number(db: Session) -> str:
        count = db.query(Appointment).count() + 1
        return f"APT-{datetime.utcnow().year}-{count:05d}"

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        appointment_date: Optional[date] = None,
        doctor_id: Optional[str] = None,
        patient_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Appointment], int]:
        query = db.query(Appointment)
        if appointment_date:
            query = query.filter(Appointment.appointment_date == appointment_date)
        if doctor_id:
            query = query.filter(Appointment.doctor_id == doctor_id)
        if patient_id:
            query = query.filter(Appointment.patient_id == patient_id)
        if status:
            query = query.filter(Appointment.status == status)

        total = query.count()
        appts = query.order_by(Appointment.appointment_date.desc(), Appointment.start_time.asc()).offset(skip).limit(limit).all()
        return appts, total

    @staticmethod
    def create(db: Session, appt_in: AppointmentCreate, created_by: Optional[str] = None) -> Appointment:
        appt_num = AppointmentService.generate_appointment_number(db)
        
        # Calculate daily token
        day_token = db.query(Appointment).filter(
            Appointment.doctor_id == appt_in.doctor_id,
            Appointment.appointment_date == appt_in.appointment_date
        ).count() + 1

        appt = Appointment(
            appointment_number=appt_num,
            token_number=day_token,
            **appt_in.model_dump(),
            created_by=created_by
        )
        db.add(appt)
        db.commit()
        db.refresh(appt)

        event_bus.publish("appointment.created", {
            "appointment_id": appt.id,
            "patient_id": appt.patient_id,
            "doctor_id": appt.doctor_id,
            "appointment_date": str(appt.appointment_date)
        })

        return appt

    @staticmethod
    def update_status(db: Session, appointment_id: str, status_in: AppointmentStatusUpdate) -> Appointment:
        appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appt:
            raise NotFoundError("Appointment not found")

        appt.status = status_in.status
        if status_in.cancellation_reason:
            appt.cancellation_reason = status_in.cancellation_reason

        # If CHECKED_IN, automatically generate or sync OPD Visit
        if status_in.status == "CHECKED_IN":
            existing_visit = db.query(OPDVisit).filter(OPDVisit.appointment_id == appt.id).first()
            if not existing_visit:
                visit_count = db.query(OPDVisit).count() + 1
                opd_visit = OPDVisit(
                    visit_number=f"OPD-{datetime.utcnow().year}-{visit_count:05d}",
                    patient_id=appt.patient_id,
                    doctor_id=appt.doctor_id,
                    department_id=appt.department_id,
                    appointment_id=appt.id,
                    queue_number=appt.token_number,
                    chief_complaint=appt.chief_complaint,
                    status="WAITING"
                )
                db.add(opd_visit)

        db.commit()
        db.refresh(appt)

        event_bus.publish(f"appointment.{status_in.status.lower()}", {
            "appointment_id": appt.id,
            "status": appt.status
        })

        return appt
