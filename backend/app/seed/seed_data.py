from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.core.config import settings
from app.modules.users.models import User, Role, Permission
from app.modules.organization.models import Organization, HospitalBranch, Department, Ward, Room, Bed

# 16 System Roles
ROLES_DATA = [
    {"name": "Super Admin", "code": "SUPER_ADMIN", "description": "Full system-wide administrative privileges", "is_system": True},
    {"name": "Hospital Admin", "code": "HOSPITAL_ADMIN", "description": "Branch and hospital administrative operations", "is_system": True},
    {"name": "Branch Admin", "code": "BRANCH_ADMIN", "description": "Branch-level management", "is_system": True},
    {"name": "Doctor / Consultant", "code": "DOCTOR", "description": "Clinical diagnosis, prescriptions, OPD/IPD orders", "is_system": True},
    {"name": "Nurse", "code": "NURSE", "description": "Patient care, vitals, MAR, shift notes", "is_system": True},
    {"name": "Receptionist", "code": "RECEPTIONIST", "description": "Patient registration, appointment scheduling, token management", "is_system": True},
    {"name": "Pharmacist", "code": "PHARMACIST", "description": "Medication dispensing, pharmacy stock, batch tracking", "is_system": True},
    {"name": "Lab Technician", "code": "LAB_TECHNICIAN", "description": "Sample collection, test processing, lab result entry", "is_system": True},
    {"name": "Radiologist", "code": "RADIOLOGIST", "description": "Radiology scheduling, imaging reports, PACS integration", "is_system": True},
    {"name": "Accountant / Cashier", "code": "ACCOUNTANT", "description": "Billing, invoices, payment collection, receipts", "is_system": True},
    {"name": "HR Manager", "code": "HR_MANAGER", "description": "Employee management, rosters, leave requests", "is_system": True},
    {"name": "Inventory Manager", "code": "INVENTORY_MANAGER", "description": "Stock tracking, transfers, adjustments", "is_system": True},
    {"name": "Procurement Officer", "code": "PROCUREMENT_OFFICER", "description": "Vendor contracts, purchase requests, POs, GRN", "is_system": True},
    {"name": "CRM Manager", "code": "CRM_MANAGER", "description": "Patient relationships, leads, inquiries, journeys", "is_system": True},
    {"name": "Marketing Manager", "code": "MARKETING_MANAGER", "description": "Campaigns, promotions, audience segmentation", "is_system": True},
    {"name": "Patient", "code": "PATIENT", "description": "Patient self-service portal access", "is_system": True},
]

MODULES_PERMS = [
    ("users", ["view", "create", "edit", "delete"]),
    ("patients", ["view", "create", "edit", "delete"]),
    ("appointments", ["view", "create", "edit", "cancel"]),
    ("clinical", ["view", "create", "edit"]),
    ("nursing", ["view", "create", "edit"]),
    ("emergency", ["view", "create", "edit"]),
    ("ot", ["view", "create", "edit"]),
    ("pharmacy", ["view", "dispense", "manage_stock"]),
    ("laboratory", ["view", "create_order", "enter_results", "validate"]),
    ("radiology", ["view", "create_order", "enter_report"]),
    ("blood_bank", ["view", "manage_stock", "transfuse"]),
    ("billing", ["view", "create_invoice", "collect_payment", "refund"]),
    ("insurance", ["view", "manage_claims"]),
    ("inventory", ["view", "manage_stock", "transfer"]),
    ("procurement", ["view", "create_po", "approve_po", "receive_grn"]),
    ("hr", ["view", "manage_staff", "approve_leave"]),
    ("crm", ["view", "manage_leads", "send_communication"]),
    ("marketing", ["view", "manage_campaigns"]),
    ("analytics", ["view_dashboards", "export_reports"]),
    ("workflows", ["view", "manage_rules"]),
    ("admin", ["manage_settings", "view_audit"]),
]

def init_db(db: Session):
    Base.metadata.create_all(bind=engine)

    # 1. Seed Permissions
    permissions_map = {}
    for module, actions in MODULES_PERMS:
        for action in actions:
            code = f"{module.upper()}:{action.upper()}"
            perm = db.query(Permission).filter(Permission.code == code).first()
            if not perm:
                perm = Permission(
                    name=f"{action.capitalize()} {module.capitalize()}",
                    code=code,
                    module=module,
                    description=f"Allows user to {action} {module}"
                )
                db.add(perm)
                db.flush()
            permissions_map[code] = perm

    # 2. Seed Roles
    roles_map = {}
    for r_data in ROLES_DATA:
        role = db.query(Role).filter(Role.code == r_data["code"]).first()
        if not role:
            role = Role(
                name=r_data["name"],
                code=r_data["code"],
                description=r_data["description"],
                is_system=r_data["is_system"]
            )
            db.add(role)
            db.flush()
        roles_map[r_data["code"]] = role

    # Assign all permissions to SUPER_ADMIN
    super_admin_role = roles_map["SUPER_ADMIN"]
    super_admin_role.permissions = list(permissions_map.values())

    # 3. Seed Default Organization
    org = db.query(Organization).filter(Organization.code == "APEX_HEALTH").first()
    if not org:
        org = Organization(
            name="Apex Global Health Institute",
            code="APEX_HEALTH",
            registration_number="MED-REG-2026-9081",
            tax_number="TAX-US-9921820",
            email="info@apexhealth.org",
            phone="+1 (555) 019-2834",
            website="https://apexhealth.org",
            address="100 Medical Center Way, Suite 500, Health City",
            currency="USD",
            timezone="UTC"
        )
        db.add(org)
        db.flush()

        # Seed Main Branch
        main_branch = HospitalBranch(
            organization_id=org.id,
            name="Apex Central Hospital",
            code="ACH-MAIN",
            is_main_branch=True,
            email="central@apexhealth.org",
            phone="+1 (555) 019-2800",
            address="100 Medical Center Way, Central Tower",
            city="Metropolis",
            state="NY",
            country="USA",
            postal_code="10001"
        )
        db.add(main_branch)
        db.flush()

        # Seed Departments
        depts_data = [
            ("General Medicine", "GEN_MED", "CLINICAL", True, True, False),
            ("Cardiology", "CARDIO", "CLINICAL", True, True, False),
            ("Orthopedics", "ORTHO", "CLINICAL", True, True, False),
            ("Pediatrics", "PEDI", "CLINICAL", True, True, False),
            ("Emergency & Trauma", "EMERGENCY", "CLINICAL", True, True, True),
            ("Diagnostic Radiology", "RADIO", "DIAGNOSTIC", False, False, False),
            ("Clinical Pathology & Lab", "LAB", "DIAGNOSTIC", False, False, False),
            ("Pharmacy Services", "PHARMACY", "SUPPORT", False, False, False),
        ]
        
        created_depts = []
        for name, code, dtype, opd, ipd, emg in depts_data:
            d = Department(
                branch_id=main_branch.id,
                name=name,
                code=code,
                department_type=dtype,
                is_opd=opd,
                is_ipd=ipd,
                is_emergency=emg
            )
            db.add(d)
            db.flush()
            created_depts.append(d)

        # Seed Wards & Beds
        gen_dept = created_depts[0]
        gen_ward = Ward(
            branch_id=main_branch.id,
            department_id=gen_dept.id,
            name="General Medical Ward A",
            code="GMW-A",
            gender_type="ALL",
            ward_type="GENERAL"
        )
        db.add(gen_ward)
        db.flush()

        icu_dept = created_depts[4]
        icu_ward = Ward(
            branch_id=main_branch.id,
            department_id=icu_dept.id,
            name="Intensive Care Unit (ICU)",
            code="ICU-1",
            gender_type="ALL",
            ward_type="ICU"
        )
        db.add(icu_ward)
        db.flush()

        # Create beds in Ward A
        for b_num in range(101, 111):
            bed = Bed(
                ward_id=gen_ward.id,
                bed_number=f"BED-{b_num}",
                status="AVAILABLE",
                bed_type="STANDARD"
            )
            db.add(bed)

        # Create beds in ICU
        for b_num in range(1, 6):
            bed = Bed(
                ward_id=icu_ward.id,
                bed_number=f"ICU-BED-{b_num}",
                status="AVAILABLE",
                bed_type="ICU"
            )
            db.add(bed)

    # 4. Seed SuperAdmin User
    admin_user = db.query(User).filter(User.email == settings.SUPERADMIN_EMAIL).first()
    if not admin_user:
        admin_user = User(
            email=settings.SUPERADMIN_EMAIL,
            username="superadmin",
            hashed_password=get_password_hash(settings.SUPERADMIN_PASSWORD),
            first_name="Super",
            last_name="Administrator",
            phone_number="+1 (555) 000-0001",
            is_verified=True,
            roles=[super_admin_role]
        )
        db.add(admin_user)

    db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
