from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.enterprise.models import BranchTransferRequest
from app.modules.enterprise.schemas import BranchTransferCreate
from app.core.exceptions import NotFoundError

class EnterpriseService:
    @staticmethod
    def get_transfers(db: Session, skip: int = 0, limit: int = 20) -> Tuple[List[BranchTransferRequest], int]:
        total = db.query(BranchTransferRequest).count()
        transfers = db.query(BranchTransferRequest).order_by(BranchTransferRequest.created_at.desc()).offset(skip).limit(limit).all()
        return transfers, total

    @staticmethod
    def create_transfer(db: Session, tr_in: BranchTransferCreate, created_by: Optional[str] = None) -> BranchTransferRequest:
        count = db.query(BranchTransferRequest).count() + 1
        transfer = BranchTransferRequest(
            transfer_code=f"XFER-{datetime.utcnow().year}-{count:04d}",
            status="REQUESTED",
            **tr_in.model_dump(),
            created_by=created_by
        )
        db.add(transfer)
        db.commit()
        db.refresh(transfer)
        return transfer
