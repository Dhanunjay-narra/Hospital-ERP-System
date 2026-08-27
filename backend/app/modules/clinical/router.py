from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.clinical.schemas import (
    PrescriptionCreate, PrescriptionResponse,
    AllergyCreate, AllergyResponse
)
from app.modules.clinical.service import ClinicalService

router = APIRouter(prefix="/clinical", tags=["Clinical & EMR"])

@router.get("/prescriptions", response_model=PaginatedResponse[PrescriptionResponse])
def list_prescriptions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    prescriptions, total = ClinicalService.get_prescriptions(db, skip=params.skip, limit=params.limit, patient_id=patient_id, doctor_id=doctor_id)
    return PaginatedResponse.create(items=prescriptions, total=total, params=params)

@router.post("/prescriptions", response_model=PrescriptionResponse)
def create_prescription(
    rx_in: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ClinicalService.create_prescription(db, rx_in, created_by=current_user.id)

@router.post("/allergies", response_model=AllergyResponse)
def add_allergy(
    allergy_in: AllergyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ClinicalService.add_allergy(db, allergy_in)

@router.get("/allergies/{patient_id}", response_model=List[AllergyResponse])
def get_patient_allergies(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ClinicalService.get_patient_allergies(db, patient_id)
