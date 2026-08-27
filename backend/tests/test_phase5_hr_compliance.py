import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_headers():
    login_res = client.post(
        "/api/v1/auth/login",
        json={
            "username_or_email": settings.SUPERADMIN_EMAIL,
            "password": settings.SUPERADMIN_PASSWORD
        }
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_hr_and_roster_flow(auth_headers):
    # Fetch a user
    users = client.get("/api/v1/users", headers=auth_headers).json()["items"]
    assert len(users) > 0
    user_id = users[0]["id"]

    # Create / get employee
    emp_res = client.post("/api/v1/hr/employees", json={
        "user_id": user_id,
        "designation": "Chief of Medicine",
        "employment_type": "FULL_TIME",
        "joining_date": "2026-01-01",
        "salary_amount": 12000.0
    }, headers=auth_headers)
    assert emp_res.status_code == 200
    emp_data = emp_res.json()
    assert "EMP-" in emp_data["employee_code"]

    # Apply leave
    leave_res = client.post("/api/v1/hr/leaves", json={
        "employee_id": emp_data["id"],
        "leave_type": "CASUAL",
        "start_date": "2026-10-01",
        "end_date": "2026-10-03",
        "reason": "Family function"
    }, headers=auth_headers)
    assert leave_res.status_code == 200

def test_medical_records_and_documents(auth_headers):
    pats = client.get("/api/v1/patients", headers=auth_headers).json()["items"]
    assert len(pats) > 0
    patient_id = pats[0]["id"]

    # Medical Record archive
    arc_res = client.post("/api/v1/medical-records/archives", json={
        "patient_id": patient_id,
        "physical_rack_number": "Rack-C-Shelf-3",
        "total_file_pages": 45,
        "retention_period_years": 10
    }, headers=auth_headers)
    assert arc_res.status_code == 200
    assert "MRD-" in arc_res.json()["archive_code"]

    # Document upload
    doc_res = client.post("/api/v1/documents", json={
        "patient_id": patient_id,
        "document_title": "Consent for Laparoscopic Surgery",
        "category": "CONSENT_FORM",
        "file_path": "/storage/consents/lap_surg_01.pdf",
        "file_size_kb": 180,
        "is_digitally_signed": True,
        "signed_by_name": "John Doe"
    }, headers=auth_headers)
    assert doc_res.status_code == 200
    assert doc_res.json()["is_digitally_signed"] == True
