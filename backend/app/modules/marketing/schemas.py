from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

class MarketingCampaignBase(BaseModel):
    campaign_name: str
    campaign_code: str
    target_demographic: str = "Adults 40+"
    budget_allocated: float = 2000.0
    start_date: date
    end_date: date
    discount_package_rate: float = 99.0

class MarketingCampaignCreate(MarketingCampaignBase):
    pass

class MarketingCampaignResponse(MarketingCampaignBase):
    id: str
    status: str
    leads_generated: int
    patients_converted: int
    created_at: datetime

    class Config:
        from_attributes = True
