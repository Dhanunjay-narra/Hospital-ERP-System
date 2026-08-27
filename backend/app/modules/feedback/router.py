from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.feedback.schemas import PatientFeedbackCreate, PatientFeedbackResponse
from app.modules.feedback.service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["Patient Feedback & NPS"])

@router.get("", response_model=PaginatedResponse[PatientFeedbackResponse])
def list_patient_feedbacks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    fbs, total = FeedbackService.get_feedbacks(db, skip=params.skip, limit=params.limit)
    return PaginatedResponse.create(items=fbs, total=total, params=params)

@router.post("", response_model=PatientFeedbackResponse)
def submit_patient_feedback(
    fb_in: PatientFeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return FeedbackService.submit_feedback(db, fb_in, created_by=current_user.id)
