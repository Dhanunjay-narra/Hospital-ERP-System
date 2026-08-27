from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.audit.service import AuditService

class AuditLogResponse(BaseModel):
    id: str
    actor_email: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

router = APIRouter(prefix="/audit", tags=["Security & Audit Logs"])

@router.get("", response_model=PaginatedResponse[AuditLogResponse])
def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    resource_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    params = PaginationParams(page=page, page_size=page_size)
    logs, total = AuditService.get_logs(db, skip=params.skip, limit=params.limit, resource_type=resource_type)
    return PaginatedResponse.create(items=logs, total=total, params=params)
