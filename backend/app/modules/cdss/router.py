from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.cdss.schemas import (
    CDSSRuleCreate, CDSSRuleResponse,
    CDSSAlertCreate, CDSSAlertResponse
)
from app.modules.cdss.service import CDSSService

router = APIRouter(prefix="/cdss", tags=["Clinical Decision Support (CDSS)"])

@router.get("/rules", response_model=List[CDSSRuleResponse])
def list_cdss_rules(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CDSSService.get_rules(db)

@router.post("/rules", response_model=CDSSRuleResponse)
def create_cdss_rule(
    rule_in: CDSSRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "DOCTOR"))
):
    return CDSSService.create_rule(db, rule_in)

@router.get("/alerts", response_model=PaginatedResponse[CDSSAlertResponse])
def list_cdss_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    alerts, total = CDSSService.get_alerts(db, skip=params.skip, limit=params.limit)
    return PaginatedResponse.create(items=alerts, total=total, params=params)

@router.post("/alerts", response_model=CDSSAlertResponse)
def record_cdss_alert(
    alert_in: CDSSAlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CDSSService.log_alert(db, alert_in, created_by=current_user.id)
