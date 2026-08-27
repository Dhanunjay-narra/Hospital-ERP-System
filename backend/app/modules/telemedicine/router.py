from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.telemedicine.schemas import TeleconsultationCreate, TeleconsultationResponse
from app.modules.telemedicine.service import TelemedicineService

router = APIRouter(prefix="/telemedicine", tags=["Virtual Telemedicine & Video"])

@router.get("/sessions", response_model=PaginatedResponse[TeleconsultationResponse])
def list_telehealth_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    sessions, total = TelemedicineService.get_sessions(db, skip=params.skip, limit=params.limit)
    return PaginatedResponse.create(items=sessions, total=total, params=params)

@router.post("/sessions", response_model=TeleconsultationResponse)
def schedule_teleconsultation(
    ses_in: TeleconsultationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TelemedicineService.create_session(db, ses_in, created_by=current_user.id)
