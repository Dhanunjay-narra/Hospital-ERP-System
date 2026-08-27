from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.marketing.schemas import MarketingCampaignCreate, MarketingCampaignResponse
from app.modules.marketing.service import MarketingService

router = APIRouter(prefix="/marketing", tags=["Marketing & Promotions"])

@router.get("/campaigns", response_model=List[MarketingCampaignResponse])
def list_campaigns(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return MarketingService.get_campaigns(db)

@router.post("/campaigns", response_model=MarketingCampaignResponse)
def create_campaign(
    cmp_in: MarketingCampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "MARKETING_HEAD"))
):
    return MarketingService.create_campaign(db, cmp_in, created_by=current_user.id)
