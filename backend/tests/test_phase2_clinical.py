import pytest
from datetime import date
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

def test_list_patients(auth_headers):
    res = client.get("/api/v1/patients", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) > 0

def test_create_and_fetch_patient(auth_headers):
    patient_payload = {
        "first_name": "Test",
        "last_name": "Patient",
        "date_of_birth": "1995-05-20",
        "gender": "MALE",
        "blood_group": "B+",
        "phone_number": "+1 (555) 999-0011",
        "email": "test.patient@example.com",
        "address": "123 Clinical Way",
        "primary_insurance_provider": "Aetna Health"
    }
    create_res = client.post("/api/v1/patients", json=patient_payload, headers=auth_headers)
    assert create_res.status_code == 200
    patient_data = create_res.json()
    assert patient_data["first_name"] == "Test"
    assert "APX-" in patient_data["uhid"]

    # Test Patient 360
    p360_res = client.get(f"/api/v1/patients/{patient_data['id']}/360", headers=auth_headers)
    assert p360_res.status_code == 200
    p360_data = p360_res.json()
    assert p360_data["patient"]["uhid"] == patient_data["uhid"]

def test_list_doctors_and_appointments(auth_headers):
    # List Doctors
    docs_res = client.get("/api/v1/doctors", headers=auth_headers)
    assert docs_res.status_code == 200
    docs = docs_res.json()["items"]
    assert len(docs) > 0

    # List Appointments
    appts_res = client.get("/api/v1/appointments", headers=auth_headers)
    assert appts_res.status_code == 200
    appts = appts_res.json()["items"]
    assert len(appts) > 0

def test_opd_and_prescriptions(auth_headers):
    # List OPD Visits
    visits_res = client.get("/api/v1/opd/visits", headers=auth_headers)
    assert visits_res.status_code == 200
    visits = visits_res.json()["items"]
    assert len(visits) > 0

    # List Clinical Prescriptions
    rx_res = client.get("/api/v1/clinical/prescriptions", headers=auth_headers)
    assert rx_res.status_code == 200
    rx_list = rx_res.json()["items"]
    assert len(rx_list) > 0
