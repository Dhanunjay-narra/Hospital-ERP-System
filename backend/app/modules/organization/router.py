from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.organization.schemas import (
    OrganizationCreate, OrganizationResponse,
    HospitalBranchCreate, HospitalBranchResponse,
    DepartmentCreate, DepartmentResponse,
    WardCreate, WardResponse,
    BedCreate, BedUpdate, BedResponse
)
from app.modules.organization.service import OrganizationService

router = APIRouter(prefix="/organization", tags=["Organization & Facilities"])

@router.get("", response_model=Optional[OrganizationResponse])
def get_organization(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return OrganizationService.get_organization(db)

@router.post("", response_model=OrganizationResponse)
def create_organization(
    org_in: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return OrganizationService.create_organization(db, org_in)

@router.get("/branches", response_model=List[HospitalBranchResponse])
def list_branches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return OrganizationService.get_branches(db)

@router.post("/branches", response_model=HospitalBranchResponse)
def create_branch(
    branch_in: HospitalBranchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return OrganizationService.create_branch(db, branch_in)

@router.get("/departments", response_model=List[DepartmentResponse])
def list_departments(
    branch_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OrganizationService.get_departments(db, branch_id)

@router.post("/departments", response_model=DepartmentResponse)
def create_department(
    dept_in: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return OrganizationService.create_department(db, dept_in)

@router.get("/wards", response_model=List[WardResponse])
def list_wards(
    branch_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OrganizationService.get_wards(db, branch_id)

@router.post("/wards", response_model=WardResponse)
def create_ward(
    ward_in: WardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return OrganizationService.create_ward(db, ward_in)

@router.get("/beds", response_model=List[BedResponse])
def list_beds(
    ward_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OrganizationService.get_beds(db, ward_id, status)

@router.post("/beds", response_model=BedResponse)
def create_bed(
    bed_in: BedCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "NURSE"))
):
    return OrganizationService.create_bed(db, bed_in)

@router.patch("/beds/{bed_id}", response_model=BedResponse)
def update_bed_status(
    bed_id: str,
    bed_update: BedUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OrganizationService.update_bed(db, bed_id, bed_update)
