from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.nursing.schemas import (
    MARCreate, MARAdministerRequest, MARResponse,
    NursingNoteCreate, NursingNoteResponse,
    IntakeOutputChartCreate, IntakeOutputChartResponse
)
from app.modules.nursing.service import NursingService

router = APIRouter(prefix="/nursing", tags=["Nursing Station"])

@router.get("/admissions/{admission_id}/mar", response_model=List[MARResponse])
def get_mar_schedule(
    admission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NursingService.get_mar_records(db, admission_id)

@router.post("/mar", response_model=MARResponse)
def schedule_dose(
    mar_in: MARCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "NURSE", "DOCTOR"))
):
    return NursingService.schedule_mar_dose(db, mar_in)

@router.patch("/mar/{mar_id}/administer", response_model=MARResponse)
def administer_dose(
    mar_id: str,
    admin_req: MARAdministerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "NURSE"))
):
    return NursingService.record_dose_administered(db, mar_id, admin_req, nurse_id=current_user.id)

@router.post("/notes", response_model=NursingNoteResponse)
def add_nursing_note(
    note_in: NursingNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "NURSE"))
):
    return NursingService.add_nursing_note(db, note_in, nurse_id=current_user.id)

@router.get("/admissions/{admission_id}/notes", response_model=List[NursingNoteResponse])
def get_nursing_notes(
    admission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NursingService.get_nursing_notes(db, admission_id)

@router.post("/intake-output", response_model=IntakeOutputChartResponse)
def record_intake_output(
    io_in: IntakeOutputChartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "NURSE"))
):
    return NursingService.record_intake_output(db, io_in, recorded_by=current_user.id)

@router.get("/admissions/{admission_id}/intake-output", response_model=List[IntakeOutputChartResponse])
def get_intake_output_history(
    admission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NursingService.get_io_charts(db, admission_id)
