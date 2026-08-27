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

def test_crm_and_communication(auth_headers):
    # Create CRM Lead
    lead_res = client.post("/api/v1/crm/leads", json={
        "full_name": "Alexander Hayes",
        "phone_number": "+1 (555) 443-8899",
        "email": "alex.hayes@example.com",
        "inquiry_specialty": "Orthopedics",
        "lead_source": "WEBSITE"
    }, headers=auth_headers)
    assert lead_res.status_code == 200
    lead_data = lead_res.json()
    assert "LEAD-" in lead_data["lead_code"]

    # Log interaction
    inter_res = client.post(f"/api/v1/crm/leads/{lead_data['id']}/interactions", json={
        "channel": "PHONE_CALL",
        "summary": "Initial counseling call completed."
    }, headers=auth_headers)
    assert inter_res.status_code == 200

    # Dispatch Message
    msg_res = client.post("/api/v1/communication/dispatch", json={
        "recipient_phone": "+1 (555) 443-8899",
        "channel": "SMS",
        "message_body": "Thank you for reaching out to Apex Health."
    }, headers=auth_headers)
    assert msg_res.status_code == 200

def test_feedback_and_telemedicine(auth_headers):
    pats = client.get("/api/v1/patients", headers=auth_headers).json()["items"]
    docs = client.get("/api/v1/doctors", headers=auth_headers).json()["items"]
    assert len(pats) > 0 and len(docs) > 0

    # Submit feedback
    fb_res = client.post("/api/v1/feedback", json={
        "patient_id": pats[0]["id"],
        "nps_score": 10,
        "doctor_care_rating": 5,
        "nursing_care_rating": 5,
        "cleanliness_rating": 5,
        "billing_experience_rating": 5,
        "comments": "Superb clinical care."
    }, headers=auth_headers)
    assert fb_res.status_code == 200

    # Telemedicine session
    tele_res = client.post("/api/v1/telemedicine/sessions", json={
        "patient_id": pats[0]["id"],
        "doctor_id": docs[0]["id"],
        "scheduled_start": "2026-08-30T10:00:00Z"
    }, headers=auth_headers)
    assert tele_res.status_code == 200
    assert "VIRT-" in tele_res.json()["session_code"]
