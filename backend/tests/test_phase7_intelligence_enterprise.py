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

def test_cdss_and_compliance(auth_headers):
    # Create CDSS Rule
    rule_res = client.post("/api/v1/cdss/rules", json={
        "rule_code": "CDSS-WARFARIN-01",
        "title": "Warfarin & NSAID Co-Prescription Hemorrhage Alert",
        "category": "DRUG_INTERACTION",
        "severity": "HIGH_CRITICAL",
        "description": "Concurrent use of Warfarin and Ibuprofen significantly elevates GI bleed risk.",
        "recommended_action": "Avoid combination or substitute with Acetaminophen."
    }, headers=auth_headers)
    assert rule_res.status_code == 200
    rule_data = rule_res.json()
    assert rule_data["rule_code"] == "CDSS-WARFARIN-01"

    # Log security event
    sec_res = client.post("/api/v1/compliance/security-events", json={
        "event_type": "AUDIT_PHI_VIEW",
        "severity": "LOW",
        "details": "User accessed Patient EMR file",
        "ip_address": "192.168.1.50"
    }, headers=auth_headers)
    assert sec_res.status_code == 200

def test_analytics_and_enterprise(auth_headers):
    # Analytics KPIs
    kpi_res = client.get("/api/v1/analytics/dashboard-kpis", headers=auth_headers)
    assert kpi_res.status_code == 200
    data = kpi_res.json()
    assert "kpis" in data
    assert "monthly_revenue_trends" in data

    # Report templates
    rpt_res = client.get("/api/v1/reports/available-templates", headers=auth_headers)
    assert rpt_res.status_code == 200
    assert len(rpt_res.json()) > 0

    # Enterprise branch transfers
    pats = client.get("/api/v1/patients", headers=auth_headers).json()["items"]
    branches = client.get("/api/v1/organization/branches", headers=auth_headers).json()
    if len(pats) > 0 and len(branches) > 0:
        src = branches[0]["id"]
        dst = branches[1]["id"] if len(branches) > 1 else branches[0]["id"]
        xfer_res = client.post("/api/v1/enterprise/transfers", json={
            "patient_id": pats[0]["id"],
            "source_branch_id": src,
            "destination_branch_id": dst,
            "clinical_reason": "Transfer for Specialized Neurosurgical Intervention",
            "requires_advanced_life_support_ambulance": True
        }, headers=auth_headers)
        assert xfer_res.status_code == 200
        assert "XFER-" in xfer_res.json()["transfer_code"]
