import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == settings.PROJECT_NAME

def test_admin_login():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username_or_email": settings.SUPERADMIN_EMAIL,
            "password": settings.SUPERADMIN_PASSWORD
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == settings.SUPERADMIN_EMAIL

def test_get_organization_facilities():
    # Login first
    login_res = client.post(
        "/api/v1/auth/login",
        json={
            "username_or_email": settings.SUPERADMIN_EMAIL,
            "password": settings.SUPERADMIN_PASSWORD
        }
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test get departments
    dept_res = client.get("/api/v1/organization/departments", headers=headers)
    assert dept_res.status_code == 200
    depts = dept_res.json()
    assert len(depts) > 0

    # Test get beds
    beds_res = client.get("/api/v1/organization/beds", headers=headers)
    assert beds_res.status_code == 200
    beds = beds_res.json()
    assert len(beds) > 0
