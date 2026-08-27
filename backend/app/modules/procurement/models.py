import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Vendor(BaseModel):
    __tablename__ = "vendors"

    vendor_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. VEN-001
    name = Column(String(200), index=True, nullable=False)
    contact_person = Column(String(100), nullable=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(Text, nullable=True)
    tax_identification_number = Column(String(100), nullable=True)
    payment_terms_days = Column(Integer, default=30, nullable=False) # Net 30, Net 60

class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    po_number = Column(String(50), unique=True, index=True, nullable=False) # e.g. PO-2026-0001
    vendor_id = Column(String(36), ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)
    warehouse_id = Column(String(36), ForeignKey("inventory_warehouses.id", ondelete="CASCADE"), nullable=False)

    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    expected_delivery_date = Column(Date, nullable=True)
    
    total_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=False)
    
    # STATUS: DRAFT, SUBMITTED, APPROVED, GOODS_RECEIVED, PARTIALLY_RECEIVED, COMPLETED, CANCELLED
    status = Column(String(50), default="SUBMITTED", index=True, nullable=False)
    payment_status = Column(String(30), default="UNPAID", nullable=False)

    vendor = relationship("Vendor", lazy="joined")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan", lazy="joined")

class PurchaseOrderItem(BaseModel):
    __tablename__ = "purchase_order_items"

    po_id = Column(String(36), ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(String(36), ForeignKey("inventory_items.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(200), nullable=False)
    quantity_ordered = Column(Integer, default=1, nullable=False)
    quantity_received = Column(Integer, default=0, nullable=False)
    unit_price = Column(Float, default=0.0, nullable=False)
    total_price = Column(Float, default=0.0, nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    item = relationship("InventoryItem", lazy="joined")
