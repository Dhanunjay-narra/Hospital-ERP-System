from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.documents.models import PatientDocument
from app.modules.documents.schemas import PatientDocumentCreate
from app.core.exceptions import NotFoundError

class DocumentService:
    @staticmethod
    def get_documents(db: Session, skip: int = 0, limit: int = 20, patient_id: Optional[str] = None, category: Optional[str] = None) -> Tuple[List[PatientDocument], int]:
        query = db.query(PatientDocument)
        if patient_id:
            query = query.filter(PatientDocument.patient_id == patient_id)
        if category:
            query = query.filter(PatientDocument.category == category)
        total = query.count()
        docs = query.order_by(PatientDocument.created_at.desc()).offset(skip).limit(limit).all()
        return docs, total

    @staticmethod
    def upload_document(db: Session, doc_in: PatientDocumentCreate, created_by: Optional[str] = None) -> PatientDocument:
        doc = PatientDocument(
            signed_at=datetime.utcnow() if doc_in.is_digitally_signed else None,
            **doc_in.model_dump(),
            created_by=created_by
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
