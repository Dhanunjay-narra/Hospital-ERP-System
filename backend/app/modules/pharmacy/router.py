from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.pharmacy.schemas import (
    MedicineCreate, MedicineResponse,
    MedicineBatchCreate, MedicineBatchResponse
)
from app.modules.pharmacy.service import PharmacyService

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy & Formulary"])

@router.get("/medicines", response_model=PaginatedResponse[MedicineResponse])
def list_medicines(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    meds, total = PharmacyService.get_all_medicines(db, skip=params.skip, limit=params.limit, search=search, category=category)
    return PaginatedResponse.create(items=meds, total=total, params=params)

@router.post("/medicines", response_model=MedicineResponse)
def create_medicine(
    med_in: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "PHARMACIST"))
):
    return PharmacyService.create_medicine(db, med_in, created_by=current_user.id)

@router.post("/medicines/{medicine_id}/batches", response_model=MedicineBatchResponse)
def add_medicine_batch(
    medicine_id: str,
    batch_in: MedicineBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "PHARMACIST"))
):
    return PharmacyService.add_batch(db, medicine_id, batch_in)
