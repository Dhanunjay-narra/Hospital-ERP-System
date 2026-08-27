from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.blood_bank.schemas import (
    BloodDonorCreate, BloodDonorResponse,
    BloodUnitCreate, BloodUnitResponse
)
from app.modules.blood_bank.service import BloodBankService

router = APIRouter(prefix="/blood-bank", tags=["Blood Bank"])

@router.get("/donors", response_model=List[BloodDonorResponse])
def list_donors(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return BloodBankService.get_donors(db)

@router.post("/donors", response_model=BloodDonorResponse)
def register_donor(
    donor_in: BloodDonorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "LAB_TECHNICIAN"))
):
    return BloodBankService.register_donor(db, donor_in, created_by=current_user.id)

@router.get("/units", response_model=List[BloodUnitResponse])
def list_blood_units(
    blood_group: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return BloodBankService.get_units(db, blood_group=blood_group, status=status)

@router.post("/units", response_model=BloodUnitResponse)
def add_blood_unit(
    unit_in: BloodUnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "LAB_TECHNICIAN"))
):
    return BloodBankService.add_unit(db, unit_in, created_by=current_user.id)
