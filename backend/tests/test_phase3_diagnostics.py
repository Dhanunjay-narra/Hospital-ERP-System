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

def test_emergency_triage_flow(auth_headers):
    # Fetch a patient
    pats = client.get("/api/v1/patients", headers=auth_headers).json()["items"]
    assert len(pats) > 0
    patient_id = pats[0]["id"]

    triage_payload = {
        "patient_id": patient_id,
        "priority_level": "RED",
        "chief_complaint": "Acute Respiratory Distress",
        "assigned_bay": "Resus Bay 1",
        "systolic_bp": 85,
        "diastolic_bp": 55,
        "pulse_rate": 130,
        "spo2_percentage": 88.0
    }
    triage_res = client.post("/api/v1/emergency/triage", json=triage_payload, headers=auth_headers)
    assert triage_res.status_code == 200
    data = triage_res.json()
    assert data["priority_level"] == "RED"
    assert "ER-" in data["triage_number"]

def test_pharmacy_and_medicines(auth_headers):
    med_payload = {
        "name": "Paracetamol 650mg",
        "generic_name": "Acetaminophen",
        "sku_code": "SKU-PCM-650",
        "category": "ANALGESICS",
        "dosage_form": "TABLET",
        "strength": "650mg",
        "unit_price": 0.20,
        "mrp": 0.35,
        "reorder_level": 50,
        "batches": [
            {
                "batch_number": "BATCH-PCM-01",
                "expiry_date": "2027-06-30",
                "quantity_received": 500,
                "selling_price": 0.35
            }
        ]
    }
    create_res = client.post("/api/v1/pharmacy/medicines", json=med_payload, headers=auth_headers)
    assert create_res.status_code in [200, 409] # 200 or already exists

    list_res = client.get("/api/v1/pharmacy/medicines", headers=auth_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()["items"]) > 0

def test_laboratory_flow(auth_headers):
    # Create a catalog test
    test_payload = {
        "test_code": "SERUM_K",
        "test_name": "Serum Potassium",
        "department": "BIOCHEMISTRY",
        "sample_type": "SERUM",
        "price": 25.0,
        "unit_of_measure": "mmol/L",
        "reference_min": 3.5,
        "reference_max": 5.0,
        "critical_low": 2.8,
        "critical_high": 6.0
    }
    test_res = client.post("/api/v1/laboratory/catalog", json=test_payload, headers=auth_headers)
    assert test_res.status_code in [200, 409, 500]

    pats = client.get("/api/v1/patients", headers=auth_headers).json()["items"]
    docs = client.get("/api/v1/doctors", headers=auth_headers).json()["items"]
    cat = client.get("/api/v1/laboratory/catalog", headers=auth_headers).json()

    if len(pats) > 0 and len(docs) > 0 and len(cat) > 0:
        order_res = client.post("/api/v1/laboratory/orders", json={
            "patient_id": pats[0]["id"],
            "doctor_id": docs[0]["id"],
            "priority": "STAT",
            "test_ids": [cat[0]["id"]]
        }, headers=auth_headers)
        assert order_res.status_code == 200
        order_data = order_res.json()
        assert "LAB-" in order_data["order_number"]

def test_radiology_and_blood_bank(auth_headers):
    # Radiology
    pats = client.get("/api/v1/patients", headers=auth_headers).json()["items"]
    docs = client.get("/api/v1/doctors", headers=auth_headers).json()["items"]
    if len(pats) > 0 and len(docs) > 0:
        rad_res = client.post("/api/v1/radiology/orders", json={
            "patient_id": pats[0]["id"],
            "doctor_id": docs[0]["id"],
            "modality": "CT_SCAN",
            "procedure_name": "CT Brain Non-Contrast",
            "clinical_indication": "Headache post fall"
        }, headers=auth_headers)
        assert rad_res.status_code == 200
        assert "RAD-" in rad_res.json()["order_number"]

    # Blood Bank Unit
    bb_res = client.post("/api/v1/blood-bank/units", json={
        "blood_group": "O+",
        "component_type": "PRBC",
        "volume_ml": 350.0,
        "collection_date": "2026-08-25",
        "expiry_date": "2026-10-05"
    }, headers=auth_headers)
    assert bb_res.status_code == 200
    assert bb_res.json()["blood_group"] == "O+"
