from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.communication.schemas import (
    CommunicationTemplateCreate, CommunicationTemplateResponse,
    DispatchedMessageCreate, DispatchedMessageResponse
)
from app.modules.communication.service import CommunicationService

router = APIRouter(prefix="/communication", tags=["Communication Engine"])

@router.get("/templates", response_model=List[CommunicationTemplateResponse])
def list_templates(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CommunicationService.get_templates(db)

@router.post("/templates", response_model=CommunicationTemplateResponse)
def create_template(
    tpl_in: CommunicationTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CommunicationService.create_template(db, tpl_in)

@router.get("/messages", response_model=PaginatedResponse[DispatchedMessageResponse])
def list_dispatched_messages(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    msgs, total = CommunicationService.get_messages(db, skip=params.skip, limit=params.limit)
    return PaginatedResponse.create(items=msgs, total=total, params=params)

@router.post("/dispatch", response_model=DispatchedMessageResponse)
def dispatch_instant_message(
    msg_in: DispatchedMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CommunicationService.dispatch_message(db, msg_in, created_by=current_user.id)
