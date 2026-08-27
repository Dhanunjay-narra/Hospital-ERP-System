from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.feedback.models import PatientFeedback
from app.modules.feedback.schemas import PatientFeedbackCreate
from app.core.exceptions import NotFoundError

class FeedbackService:
    @staticmethod
    def get_feedbacks(db: Session, skip: int = 0, limit: int = 20) -> Tuple[List[PatientFeedback], int]:
        total = db.query(PatientFeedback).count()
        feedbacks = db.query(PatientFeedback).order_by(PatientFeedback.created_at.desc()).offset(skip).limit(limit).all()
        return feedbacks, total

    @staticmethod
    def submit_feedback(db: Session, fb_in: PatientFeedbackCreate, created_by: Optional[str] = None) -> PatientFeedback:
        fb = PatientFeedback(
            grievance_resolved=False,
            **fb_in.model_dump(),
            created_by=created_by
        )
        db.add(fb)
        db.commit()
        db.refresh(fb)
        return fb
