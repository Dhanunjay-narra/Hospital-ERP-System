from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.organization.models import (
    Organization, HospitalBranch, Building, Floor, Department, Ward, Room, Bed
)
from app.modules.organization.schemas import (
    OrganizationCreate, HospitalBranchCreate, DepartmentCreate, WardCreate, RoomCreate, BedCreate, BedUpdate
)
from app.core.exceptions import NotFoundError, ConflictError

class OrganizationService:
    @staticmethod
    def get_organization(db: Session) -> Optional[Organization]:
        return db.query(Organization).first()

    @staticmethod
    def create_organization(db: Session, org_in: OrganizationCreate) -> Organization:
        existing = db.query(Organization).filter(Organization.code == org_in.code).first()
        if existing:
            raise ConflictError("Organization with this code already exists")
        org = Organization(**org_in.model_dump())
        db.add(org)
        db.commit()
        db.refresh(org)
        return org

    @staticmethod
    def get_branches(db: Session) -> List[HospitalBranch]:
        return db.query(HospitalBranch).all()

    @staticmethod
    def create_branch(db: Session, branch_in: HospitalBranchCreate) -> HospitalBranch:
        branch = HospitalBranch(**branch_in.model_dump())
        db.add(branch)
        db.commit()
        db.refresh(branch)
        return branch

    @staticmethod
    def get_departments(db: Session, branch_id: Optional[str] = None) -> List[Department]:
        query = db.query(Department)
        if branch_id:
            query = query.filter(Department.branch_id == branch_id)
        return query.all()

    @staticmethod
    def create_department(db: Session, dept_in: DepartmentCreate) -> Department:
        dept = Department(**dept_in.model_dump())
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept

    @staticmethod
    def get_wards(db: Session, branch_id: Optional[str] = None) -> List[Ward]:
        query = db.query(Ward)
        if branch_id:
            query = query.filter(Ward.branch_id == branch_id)
        return query.all()

    @staticmethod
    def create_ward(db: Session, ward_in: WardCreate) -> Ward:
        ward = Ward(**ward_in.model_dump())
        db.add(ward)
        db.commit()
        db.refresh(ward)
        return ward

    @staticmethod
    def get_beds(db: Session, ward_id: Optional[str] = None, status: Optional[str] = None) -> List[Bed]:
        query = db.query(Bed)
        if ward_id:
            query = query.filter(Bed.ward_id == ward_id)
        if status:
            query = query.filter(Bed.status == status)
        return query.all()

    @staticmethod
    def create_bed(db: Session, bed_in: BedCreate) -> Bed:
        bed = Bed(**bed_in.model_dump())
        db.add(bed)
        db.commit()
        db.refresh(bed)
        return bed

    @staticmethod
    def update_bed(db: Session, bed_id: str, bed_update: BedUpdate) -> Bed:
        bed = db.query(Bed).filter(Bed.id == bed_id).first()
        if not bed:
            raise NotFoundError("Bed not found")
        for key, val in bed_update.model_dump(exclude_unset=True).items():
            setattr(bed, key, val)
        db.commit()
        db.refresh(bed)
        return bed
