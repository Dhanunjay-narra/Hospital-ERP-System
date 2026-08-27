# ApexCare Hospital ERP & CRM Enterprise Platform

[![CI/CD Pipeline](https://github.com/Dhanunjay-narra/Hospital-ERP-System/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Dhanunjay-narra/Hospital-ERP-System/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.115-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014.2-black.svg)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2016-336791.svg)](https://www.postgresql.org)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript%205.0-3178c6.svg)](https://www.typescriptlang.org)

**ApexCare** is an enterprise-grade, comprehensive Hospital ERP + Patient CRM software platform engineered as a modular monolith with **33 decoupled domain modules**. It provides a unified system for clinical workflows, electronic medical records, diagnostic departments, acute care, billing & insurance, pharmacy, supply chain, staff management, patient CRM engagement, and executive business intelligence.

---

## 🏥 Complete 33-Module Domain Architecture

| Pillar | Domain Modules | Key Capabilities |
| :--- | :--- | :--- |
| **I. Platform Foundation** | `01. Auth` • `02. Users & RBAC` • `Organization` • `Audit` | JWT tokens, 16 granular roles, branch/building/ward hierarchy, immutable audit logs. |
| **II. Patient Operations** | `03. Patients` • `04. Doctors` • `05. Appointments` • `06. OPD` • `07. IPD` • `08. Clinical EMR` • `09. Nursing` | UHID 360°, doctor matrices, token queuing, ICD-10 coding, bed ledger, MAR chart, intake/output. |
| **III. Diagnostics & Acute Care** | `10. Emergency (ESI)` • `11. Operation Theatre` • `12. Pharmacy` • `13. Laboratory` • `14. Radiology` • `15. Blood Bank` | 5-level triage, WHO surgical checklist, batch expiry tracker, panic lab alerts, PACS/DICOM, cold-chain units. |
| **IV. Finance & Supply Chain** | `16. Billing & POS` • `17. Insurance (TPA)` • `18. Inventory` • `19. Procurement` | Auto-aggregated invoices, electronic EDI claims, multi-store stock, POs, goods receipt (GRN). |
| **V. Staff & Compliance** | `20. Staff & HR` • `21. Duty Roster` • `22. Medical Records (MRD)` • `23. Consents & Docs` | Employee profiles, 24/7 roster, SBAR handovers, physical rack indexing, e-signed consent vault. |
| **VI. CRM & Telehealth** | `24. Patient CRM` • `25. Communication` • `26. Marketing` • `27. Feedback (NPS)` • `28. Telemedicine` | Inquiry pipeline, SMS/WhatsApp engine, health camp packages, 5-star NPS rating, WebRTC video rooms. |
| **VII. Intelligence & Enterprise** | `29. CDSS Rules` • `30. Executive BI` • `31. Reports Engine` • `32. HIPAA Security` • `33. Multi-Branch` | Drug-drug interaction rules, Recharts KPIs, dynamic PDF/CSV exports, ALS ambulance transfer dispatch. |

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- Python 3.11+
- Node.js 20+ & npm
- PostgreSQL 16 & Redis 7 (or SQLite for development)

### 1. Backend Setup
```bash
cd backend
python -m venv .venv

# Windows Powershell
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

# Initialize Database & Seed Master Data
python -m app.seed.seed_data

# Run API Server
uvicorn app.main:app --reload --port 8000
```
- Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Interactive ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
- Web Application: [http://localhost:3000](http://localhost:3000)

### 3. Default Demo Credentials
- **Super Administrator**: `admin@apexcare.health` / `ApexAdmin@2026`

---

## 🐳 Docker Deployment

To launch the full production environment (PostgreSQL 16, Redis 7, Backend API, Next.js Frontend, Nginx Gateway):

```bash
docker-compose up --build -d
```
Access the application at [http://localhost](http://localhost).

---

## 🧪 Testing Suite

Run the full automated test suite covering all 33 domains:
```bash
cd backend
pytest -v
```

Run frontend static type checking:
```bash
cd frontend
npx tsc --noEmit
```

---

## 📄 License
This project is licensed under the MIT License.
