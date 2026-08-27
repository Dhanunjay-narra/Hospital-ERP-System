from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.documents.schemas import PatientDocumentCreate, PatientDocumentResponse
from app.modules.documents.service import DocumentService

router = APIRouter(prefix="/documents", tags=["Document Management & Consents"])

@router.get("", response_model=PaginatedResponse[PatientDocumentResponse])
def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    docs, total = DocumentService.get_documents(db, skip=params.skip, limit=params.limit, patient_id=patient_id, category=category)
    return PaginatedResponse.create(items=docs, total=total, params=params)

@router.post("", response_model=PatientDocumentResponse)
def upload_document(
    doc_in: PatientDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return DocumentService.upload_document(db, doc_in, created_by=current_user.id)
