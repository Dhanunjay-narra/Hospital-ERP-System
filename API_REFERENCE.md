# ApexCare Hospital ERP + CRM API Specification Reference

All endpoints are prefixed with `/api/v1` and protected by standard JWT Bearer Authorization headers (`Authorization: Bearer <token>`).

## Core Endpoints Summary

### Authentication & Access
- `POST /api/v1/auth/login`: Authenticate credentials, return JWT access token.
- `GET /api/v1/auth/me`: Current user session and permissions profile.

### Patients & Clinical Operations
- `GET /api/v1/patients`: List patients (paginated, search by UHID/Name/Phone).
- `POST /api/v1/patients`: Register new patient, auto-generates UHID (`APX-YYYY-XXXXX`).
- `GET /api/v1/patients/{id}/360`: Complete clinical 360-degree patient timeline.
- `GET /api/v1/doctors`: Directory of medical specialists & weekly schedules.
- `POST /api/v1/appointments`: Book appointment with token queue number.
- `POST /api/v1/opd/visits`: Record OPD consultation, ICD-10 diagnosis, vitals.
- `POST /api/v1/ipd/admissions`: Inpatient bed allocation & admission desk.
- `POST /api/v1/clinical/prescriptions`: Issue electronic prescription with dosage/frequency.
- `POST /api/v1/nursing/mar`: Record Medication Administration Record (MAR).

### Diagnostics & Acute Care
- `POST /api/v1/emergency/triage`: Manchester/ESI 5-level emergency intake.
- `POST /api/v1/ot/surgeries`: Schedule operating theater and assign surgeons.
- `GET /api/v1/pharmacy/medicines`: Drug formulary and batch expiry levels.
- `POST /api/v1/laboratory/orders`: Diagnostic test order with barcode accessioning.
- `POST /api/v1/radiology/orders`: Imaging study request (X-Ray, CT, MRI).
- `POST /api/v1/blood-bank/units`: Register blood units & cross-match stock.

### Finance, Insurance & Supply Chain
- `POST /api/v1/billing/invoices`: Aggregate itemized services into official invoice.
- `POST /api/v1/billing/payments`: Process payment (Cash, Card, UPI, Insurance) and issue receipt.
- `POST /api/v1/insurance/claims`: Electronic EDI claim submission.
- `POST /api/v1/inventory/items`: Store stock ledger and reorder alerts.
- `POST /api/v1/procurement/purchase-orders`: Generate vendor purchase orders.

### Staff, CRM, Intelligence & Enterprise
- `POST /api/v1/hr/employees`: Employee onboarding and compensation records.
- `POST /api/v1/roster/slots`: Department duty shift allocations.
- `POST /api/v1/crm/leads`: Patient inquiry intake and counselor logging.
- `POST /api/v1/communication/dispatch`: Send SMS, WhatsApp or Email notification.
- `POST /api/v1/telemedicine/sessions`: Generate encrypted WebRTC video room.
- `GET /api/v1/analytics/dashboard-kpis`: Real-time hospital business intelligence metrics.
- `GET /api/v1/reports/generate/{id}`: Export institutional reports in CSV/PDF format.
- `POST /api/v1/enterprise/transfers`: Coordinate inter-hospital ALS ambulance transfers.
