import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class MedicineMaster(BaseModel):
    __tablename__ = "medicines"

    name = Column(String(200), index=True, nullable=False) # Brand Name e.g. Augmentin 625mg
    generic_name = Column(String(200), index=True, nullable=False) # e.g. Amoxicillin + Clavulanic Acid
    sku_code = Column(String(50), unique=True, index=True, nullable=False)
    category = Column(String(100), default="ANTIBIOTICS", nullable=False) # ANTIBIOTICS, ANALGESICS, CARDIOVASCULAR, etc.
    dosage_form = Column(String(50), default="TABLET", nullable=False) # TABLET, CAPSULE, SYRUP, INJECTION, OINTMENT
    strength = Column(String(50), nullable=False) # 625mg, 500mg, 10mg/ml
    manufacturer = Column(String(150), nullable=True)
    
    unit_price = Column(Float, default=1.0, nullable=False)
    mrp = Column(Float, default=1.5, nullable=False)
    reorder_level = Column(Integer, default=100, nullable=False)
    is_prescription_required = Column(Boolean, default=True, nullable=False)
    is_narcotic = Column(Boolean, default=False, nullable=False)

    batches = relationship("MedicineBatch", back_populates="medicine", cascade="all, delete-orphan")

class MedicineBatch(BaseModel):
    __tablename__ = "medicine_batches"

    medicine_id = Column(String(36), ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False)
    batch_number = Column(String(100), index=True, nullable=False)
    expiry_date = Column(Date, index=True, nullable=False)
    manufacturing_date = Column(Date, nullable=True)
    
    quantity_received = Column(Integer, default=0, nullable=False)
    quantity_available = Column(Integer, default=0, nullable=False)
    purchase_rate = Column(Float, default=0.0, nullable=False)
    selling_price = Column(Float, default=0.0, nullable=False)
    storage_location = Column(String(100), default="Aisle 1 - Shelf A", nullable=True)

    medicine = relationship("MedicineMaster", back_populates="batches", lazy="joined")
