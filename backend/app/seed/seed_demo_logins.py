from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.modules.organization.models import Organization, HospitalBranch
from app.modules.users.models import User, Role

db = SessionLocal()

demo_users = [
    ("admin@hospital.com", "admin", "Admin@123456", "Super", "Administrator", "SUPER_ADMIN"),
    ("doctor@hospital.com", "doctor", "Doctor@123456", "Dr. Robert", "Vance", "DOCTOR"),
    ("nurse@hospital.com", "nurse", "Nurse@123456", "Sarah", "Connor", "NURSE"),
    ("billing@hospital.com", "billing", "Billing@123456", "James", "Wilson", "ACCOUNTANT"),
    ("reception@hospital.com", "reception", "Reception@123456", "Emily", "Watson", "RECEPTIONIST"),
]

for email, username, pwd, fn, ln, role_code in demo_users:
    u = db.query(User).filter(User.email == email).first()
    r = db.query(Role).filter(Role.code == role_code).first()
    if not u:
        u = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(pwd),
            first_name=fn,
            last_name=ln,
            is_verified=True,
            is_active=True,
            roles=[r] if r else []
        )
        db.add(u)
        print(f"Created demo user: {email} / {pwd} [{role_code}]")
    else:
        u.hashed_password = get_password_hash(pwd)
        u.is_active = True
        if r and r not in u.roles:
            u.roles.append(r)
        print(f"Updated demo user: {email} / {pwd} [{role_code}]")

db.commit()
db.close()
print("All demo user accounts are successfully ready for 1-click login.")
