import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.database import Base, engine, SessionLocal
from app.seed.seed_data import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("hospital_erp")

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Comprehensive Hospital ERP + CRM Multi-tenant Platform API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_code": exc.error_code,
            "detail": exc.detail,
            "data": exc.data
        }
    )

@app.on_event("startup")
def on_startup():
    logger.info("Initializing Hospital ERP + CRM Database...")
    db = SessionLocal()
    try:
        init_db(db)
        logger.info("Hospital ERP + CRM Ready.")
    finally:
        db.close()

# Health Check
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }

# Phase 1 Routers
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router, roles_router
from app.modules.organization.router import router as org_router
from app.modules.audit.router import router as audit_router

# Phase 2 Routers
from app.modules.patients.router import router as patients_router
from app.modules.doctors.router import router as doctors_router
from app.modules.appointments.router import router as appointments_router
from app.modules.opd.router import router as opd_router
from app.modules.ipd.router import router as ipd_router
from app.modules.clinical.router import router as clinical_router
from app.modules.nursing.router import router as nursing_router

# Phase 3 Routers
from app.modules.emergency.router import router as emergency_router
from app.modules.ot.router import router as ot_router
from app.modules.pharmacy.router import router as pharmacy_router
from app.modules.laboratory.router import router as laboratory_router
from app.modules.radiology.router import router as radiology_router
from app.modules.blood_bank.router import router as blood_bank_router

# Phase 4 Routers
from app.modules.billing.router import router as billing_router
from app.modules.insurance.router import router as insurance_router
from app.modules.inventory.router import router as inventory_router
from app.modules.procurement.router import router as procurement_router

# Phase 5 Routers
from app.modules.hr.router import router as hr_router
from app.modules.roster.router import router as roster_router
from app.modules.medical_records.router import router as medical_records_router
from app.modules.documents.router import router as documents_router

# Phase 6 Routers
from app.modules.crm.router import router as crm_router
from app.modules.communication.router import router as communication_router
from app.modules.marketing.router import router as marketing_router
from app.modules.feedback.router import router as feedback_router
from app.modules.telemedicine.router import router as telemedicine_router

# Include All Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(roles_router, prefix=settings.API_V1_STR)
app.include_router(org_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)
app.include_router(patients_router, prefix=settings.API_V1_STR)
app.include_router(doctors_router, prefix=settings.API_V1_STR)
app.include_router(appointments_router, prefix=settings.API_V1_STR)
app.include_router(opd_router, prefix=settings.API_V1_STR)
app.include_router(ipd_router, prefix=settings.API_V1_STR)
app.include_router(clinical_router, prefix=settings.API_V1_STR)
app.include_router(nursing_router, prefix=settings.API_V1_STR)
app.include_router(emergency_router, prefix=settings.API_V1_STR)
app.include_router(ot_router, prefix=settings.API_V1_STR)
app.include_router(pharmacy_router, prefix=settings.API_V1_STR)
app.include_router(laboratory_router, prefix=settings.API_V1_STR)
app.include_router(radiology_router, prefix=settings.API_V1_STR)
app.include_router(blood_bank_router, prefix=settings.API_V1_STR)
app.include_router(billing_router, prefix=settings.API_V1_STR)
app.include_router(insurance_router, prefix=settings.API_V1_STR)
app.include_router(inventory_router, prefix=settings.API_V1_STR)
app.include_router(procurement_router, prefix=settings.API_V1_STR)
app.include_router(hr_router, prefix=settings.API_V1_STR)
app.include_router(roster_router, prefix=settings.API_V1_STR)
app.include_router(medical_records_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)
app.include_router(crm_router, prefix=settings.API_V1_STR)
app.include_router(communication_router, prefix=settings.API_V1_STR)
app.include_router(marketing_router, prefix=settings.API_V1_STR)
app.include_router(feedback_router, prefix=settings.API_V1_STR)
app.include_router(telemedicine_router, prefix=settings.API_V1_STR)
