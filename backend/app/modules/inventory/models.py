import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class InventoryWarehouse(BaseModel):
    __tablename__ = "inventory_warehouses"

    name = Column(String(150), nullable=False) # Central Medical Store, Surgical Store, Ward Sub-store
    code = Column(String(50), unique=True, index=True, nullable=False)
    location = Column(String(200), nullable=True) # Basement Level 1
    manager_user_id = Column(String(36), nullable=True)

class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"

    item_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. ITM-SYRINGE-10ML, ITM-SURG-GLOVES
    item_name = Column(String(200), index=True, nullable=False)
    category = Column(String(100), default="CONSUMABLES", nullable=False) # CONSUMABLES, SURGICAL_INSTRUMENTS, LINEN, PPE, STATIONERY
    unit_of_measure = Column(String(30), default="BOX", nullable=False) # PCS, BOX, PACK, ROLL, KG
    
    warehouse_id = Column(String(36), ForeignKey("inventory_warehouses.id", ondelete="CASCADE"), nullable=False)
    quantity_on_hand = Column(Integer, default=0, nullable=False)
    reorder_threshold = Column(Integer, default=50, nullable=False)
    unit_cost = Column(Float, default=1.0, nullable=False)
    
    warehouse = relationship("InventoryWarehouse", lazy="joined")
