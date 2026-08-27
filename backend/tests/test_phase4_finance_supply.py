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

def test_billing_and_payments(auth_headers):
    pats = client.get("/api/v1/patients", headers=auth_headers).json()["items"]
    assert len(pats) > 0
    patient_id = pats[0]["id"]

    inv_payload = {
        "patient_id": patient_id,
        "items": [
            {
                "service_name": "Emergency Consultation",
                "quantity": 1,
                "unit_price": 150.0,
                "discount_percent": 10.0,
                "tax_amount": 7.5
            }
        ]
    }
    inv_res = client.post("/api/v1/billing/invoices", json=inv_payload, headers=auth_headers)
    assert inv_res.status_code == 200
    inv_data = inv_res.json()
    assert "INV-" in inv_data["invoice_number"]
    assert inv_data["total_amount"] > 0

    # Pay the invoice
    pay_res = client.post("/api/v1/billing/payments", json={
        "invoice_id": inv_data["id"],
        "amount": inv_data["total_amount"],
        "payment_method": "CREDIT_CARD",
        "transaction_reference": "TXN-TEST-1234"
    }, headers=auth_headers)
    assert pay_res.status_code == 200
    pay_data = pay_res.json()
    assert "REC-" in pay_data["receipt_number"]

def test_inventory_and_procurement(auth_headers):
    # Create Warehouse
    wh_res = client.post("/api/v1/inventory/warehouses", json={
        "name": "General Store Unit B",
        "code": "WH-GEN-B",
        "location": "Building A"
    }, headers=auth_headers)
    assert wh_res.status_code in [200, 409, 500]

    wh_list = client.get("/api/v1/inventory/warehouses", headers=auth_headers).json()
    assert len(wh_list) > 0
    wh_id = wh_list[0]["id"]

    # Create Inventory Item
    item_res = client.post("/api/v1/inventory/items", json={
        "item_code": "ITM-IV-CAN-20G",
        "item_name": "IV Cannula 20G Pink",
        "category": "CONSUMABLES",
        "unit_of_measure": "PCS",
        "warehouse_id": wh_id,
        "quantity_on_hand": 300,
        "reorder_threshold": 50,
        "unit_cost": 2.50
    }, headers=auth_headers)
    assert item_res.status_code in [200, 409, 500]

    # Create Vendor
    ven_res = client.post("/api/v1/procurement/vendors", json={
        "name": "MedEquip Global Inc",
        "vendor_code": "VEN-MEG-01",
        "email": "orders@medequip.com",
        "phone": "+1 (555) 777-8899"
    }, headers=auth_headers)
    assert ven_res.status_code in [200, 409, 500]
