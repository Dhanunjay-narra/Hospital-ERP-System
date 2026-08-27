from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.appointments.schemas import AppointmentCreate, AppointmentStatusUpdate, AppointmentResponse
from app.modules.appointments.service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointment Lifecycle"])

@router.get("", response_model=PaginatedResponse[AppointmentResponse])
def list_appointments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    appointment_date: Optional[date] = None,
    doctor_id: Optional[str] = None,
    patient_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    appts, total = AppointmentService.get_all(
        db,
        skip=params.skip,
        limit=params.limit,
        appointment_date=appointment_date,
        doctor_id=doctor_id,
        patient_id=patient_id,
        status=status
    )
    return PaginatedResponse.create(items=appts, total=total, params=params)

@router.post("", response_model=AppointmentResponse)
def book_appointment(
    appt_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AppointmentService.create(db, appt_in, created_by=current_user.id)

@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment_status(
    appointment_id: str,
    status_in: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AppointmentService.update_status(db, appointment_id, status_in)
