from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.marketing.models import MarketingCampaign
from app.modules.marketing.schemas import MarketingCampaignCreate
from app.core.exceptions import NotFoundError

class MarketingService:
    @staticmethod
    def get_campaigns(db: Session) -> List[MarketingCampaign]:
        return db.query(MarketingCampaign).order_by(MarketingCampaign.start_date.desc()).all()

    @staticmethod
    def create_campaign(db: Session, cmp_in: MarketingCampaignCreate, created_by: Optional[str] = None) -> MarketingCampaign:
        existing = db.query(MarketingCampaign).filter(MarketingCampaign.campaign_code == cmp_in.campaign_code).first()
        if existing:
            return existing
        cmp = MarketingCampaign(
            status="ACTIVE",
            **cmp_in.model_dump(),
            created_by=created_by
        )
        db.add(cmp)
        db.commit()
        db.refresh(cmp)
        return cmp
