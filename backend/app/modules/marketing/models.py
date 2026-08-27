import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class MarketingCampaign(BaseModel):
    __tablename__ = "marketing_campaigns"

    campaign_name = Column(String(200), nullable=False) # World Heart Day Comprehensive Cardiac Screening
    campaign_code = Column(String(50), unique=True, index=True, nullable=False) # CMP-2026-CARDIO
    target_demographic = Column(String(100), default="Adults 40+", nullable=False)
    budget_allocated = Column(Float, default=2000.0, nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # STATUS: PLANNED, ACTIVE, COMPLETED, CANCELLED
    status = Column(String(30), default="ACTIVE", index=True, nullable=False)
    discount_package_rate = Column(Float, default=99.0, nullable=False)
    leads_generated = Column(Integer, default=0, nullable=False)
    patients_converted = Column(Integer, default=0, nullable=False)
