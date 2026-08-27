import datetime
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.core.config import settings
from app.modules.users.models import User, Role, Permission
from app.modules.organization.models import Organization, HospitalBranch, Department, Ward, Room, Bed
from app.modules.doctors.models import Doctor, DoctorSchedule
from app.modules.patients.models import Patient
from app.modules.appointments.models import Appointment
from app.modules.opd.models import OPDVisit, VitalSigns
from app.modules.ipd.models import Admission, DailyClinicalRound
from app.modules.clinical.models import Prescription, PrescriptionItem, Allergy

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

    # 1. Seed Permissions & Roles
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

    super_admin_role = roles_map["SUPER_ADMIN"]
    super_admin_role.permissions = list(permissions_map.values())

    # 2. Seed Organization & Branch
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

    main_branch = db.query(HospitalBranch).filter(HospitalBranch.code == "ACH-MAIN").first()
    if not main_branch:
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

    # 3. Seed Departments
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
    created_depts = {}
    for name, code, dtype, opd, ipd, emg in depts_data:
        d = db.query(Department).filter(Department.code == code).first()
        if not d:
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
        created_depts[code] = d

    # 4. Seed Wards & Beds
    gen_ward = db.query(Ward).filter(Ward.code == "GMW-A").first()
    if not gen_ward:
        gen_ward = Ward(
            branch_id=main_branch.id,
            department_id=created_depts["GEN_MED"].id,
            name="General Medical Ward A",
            code="GMW-A",
            gender_type="ALL",
            ward_type="GENERAL"
        )
        db.add(gen_ward)
        db.flush()
        for b_num in range(101, 111):
            bed = Bed(ward_id=gen_ward.id, bed_number=f"BED-{b_num}", status="AVAILABLE", bed_type="STANDARD")
            db.add(bed)

    icu_ward = db.query(Ward).filter(Ward.code == "ICU-1").first()
    if not icu_ward:
        icu_ward = Ward(
            branch_id=main_branch.id,
            department_id=created_depts["EMERGENCY"].id,
            name="Intensive Care Unit (ICU)",
            code="ICU-1",
            gender_type="ALL",
            ward_type="ICU"
        )
        db.add(icu_ward)
        db.flush()
        for b_num in range(1, 6):
            bed = Bed(ward_id=icu_ward.id, bed_number=f"ICU-BED-{b_num}", status="AVAILABLE", bed_type="ICU")
            db.add(bed)

    # 5. Seed SuperAdmin User
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
        db.flush()

    # 6. Seed Sample Doctors
    doc_role = roles_map["DOCTOR"]
    doctors_info = [
        ("Dr. Robert", "Vance", "vance@hospital.com", "vance", "DOC-101", "LIC-NY-9921", "Cardiology", "MD, FACC", 14, "CARDIO", "Room 201", 150.0),
        ("Dr. Elena", "Rostova", "rostova@hospital.com", "rostova", "DOC-102", "LIC-NY-8812", "Orthopedics", "MS, FRCS", 11, "ORTHO", "Room 204", 120.0),
        ("Dr. Marcus", "Brody", "brody@hospital.com", "brody", "DOC-103", "LIC-NY-7734", "General Medicine", "MD (Internal Med)", 18, "GEN_MED", "Room 102", 100.0),
    ]
    created_docs = []
    for f_name, l_name, email, uname, code, lic, spec, qual, exp, dept_code, room, fee in doctors_info:
        u = db.query(User).filter(User.email == email).first()
        if not u:
            u = User(
                email=email,
                username=uname,
                hashed_password=get_password_hash("Doctor@123"),
                first_name=f_name,
                last_name=l_name,
                phone_number="+1 (555) 123-4567",
                is_verified=True,
                roles=[doc_role]
            )
            db.add(u)
            db.flush()
        doc = db.query(Doctor).filter(Doctor.doctor_code == code).first()
        if not doc:
            doc = Doctor(
                doctor_code=code,
                user_id=u.id,
                license_number=lic,
                specialization=spec,
                qualification=qual,
                experience_years=exp,
                department_id=created_depts[dept_code].id,
                consultation_room=room,
                consultation_fee=fee,
                follow_up_fee=fee * 0.5
            )
            db.add(doc)
            db.flush()
            for day in range(0, 5): # Mon-Fri
                sched = DoctorSchedule(
                    doctor_id=doc.id,
                    day_of_week=day,
                    start_time="09:00",
                    end_time="17:00",
                    max_patients=25
                )
                db.add(sched)
        created_docs.append(doc)

    # 7. Seed Patients
    patients_data = [
        ("Sarah", "Jenkins", date(1988, 4, 15), "FEMALE", "O+", "+1 (555) 234-5678", "sarah.j@example.com", "45 Elm St, Metropolis", "Penicillin allergy"),
        ("Michael", "Chen", date(1975, 9, 23), "MALE", "A+", "+1 (555) 345-6789", "mchen@example.com", "88 Pine St, Metropolis", "Hypertension"),
        ("Amanda", "Foster", date(1992, 11, 8), "FEMALE", "B+", "+1 (555) 456-7890", "afoster@example.com", "12 Maple Ave, Metropolis", "None"),
        ("David", "Miller", date(1960, 2, 19), "MALE", "AB-", "+1 (555) 567-8901", "dmiller@example.com", "77 Oak Lane, Metropolis", "Type 2 Diabetes"),
    ]
    created_patients = []
    for i, (fn, ln, dob, g, bg, ph, em, addr, med_hist) in enumerate(patients_data):
        uhid = f"APX-2026-{i+1:05d}"
        p = db.query(Patient).filter(Patient.uhid == uhid).first()
        if not p:
            p = Patient(
                uhid=uhid,
                first_name=fn,
                last_name=ln,
                date_of_birth=dob,
                gender=g,
                blood_group=bg,
                phone_number=ph,
                email=em,
                address=addr,
                allergies_summary=med_hist,
                primary_insurance_provider="BlueCross Shield",
                insurance_policy_number=f"POL-99{i+1}82"
            )
            db.add(p)
            db.flush()
        created_patients.append(p)

    # 8. Seed Appointments & OPD Visits
    if created_docs and created_patients:
        doc1 = created_docs[0]
        pat1 = created_patients[0]

        appt = db.query(Appointment).filter(Appointment.appointment_number == "APT-2026-00001").first()
        if not appt:
            appt = Appointment(
                appointment_number="APT-2026-00001",
                patient_id=pat1.id,
                doctor_id=doc1.id,
                department_id=doc1.department_id,
                appointment_date=date.today(),
                start_time="10:00",
                end_time="10:15",
                token_number=1,
                status="CHECKED_IN",
                chief_complaint="Palpitations and shortness of breath during exertion",
                consultation_fee=doc1.consultation_fee,
                is_paid=True
            )
            db.add(appt)
            db.flush()

            opd_visit = OPDVisit(
                visit_number="OPD-2026-00001",
                patient_id=pat1.id,
                doctor_id=doc1.id,
                department_id=doc1.department_id,
                appointment_id=appt.id,
                queue_number=1,
                status="IN_CONSULTATION",
                chief_complaint=appt.chief_complaint
            )
            db.add(opd_visit)
            db.flush()

            # Add vitals
            vitals = VitalSigns(
                patient_id=pat1.id,
                opd_visit_id=opd_visit.id,
                systolic_bp=128,
                diastolic_bp=84,
                pulse_rate=78,
                temperature_celsius=36.8,
                spo2_percentage=98.5,
                height_cm=168.0,
                weight_kg=64.0,
                bmi=22.7
            )
            db.add(vitals)

            # Add Prescription
            rx = Prescription(
                prescription_number="RX-2026-00001",
                patient_id=pat1.id,
                doctor_id=doc1.id,
                opd_visit_id=opd_visit.id,
                diagnosis_notes="Mild sinus tachycardia. Normal baseline ECG.",
                general_advice="Adequate hydration, reduce caffeine intake, follow up in 2 weeks.",
                status="PENDING_DISPENSE"
            )
            db.add(rx)
            db.flush()

            item1 = PrescriptionItem(
                prescription_id=rx.id,
                medicine_name="Metoprolol Succinate 25mg",
                generic_name="Metoprolol",
                dosage="25mg",
                frequency="1-0-0",
                duration_days=14,
                route="ORAL",
                timing_instructions="Morning after breakfast",
                total_quantity=14
            )
            db.add(item1)

    db.commit()
    print("Clinical seed data populated successfully.")
