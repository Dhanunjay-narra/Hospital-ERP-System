from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class VendorBase(BaseModel):
    name: str
    vendor_code: str
    contact_person: Optional[str] = None
    email: str
    phone: str
    address: Optional[str] = None
    payment_terms_days: int = 30

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    id: str

    class Config:
        from_attributes = True

class PurchaseOrderItemCreate(BaseModel):
    item_id: str
    item_name: str
    quantity_ordered: int = 1
    unit_price: float

class PurchaseOrderItemResponse(PurchaseOrderItemCreate):
    id: str
    quantity_received: int
    total_price: float

    class Config:
        from_attributes = True

class PurchaseOrderCreate(BaseModel):
    vendor_id: str
    warehouse_id: str
    expected_delivery_date: Optional[date] = None
    items: List[PurchaseOrderItemCreate]

class PurchaseOrderResponse(BaseModel):
    id: str
    po_number: str
    total_amount: float
    tax_amount: float
    grand_total: float
    status: str
    payment_status: str
    order_date: datetime
    vendor: Optional[VendorResponse] = None
    items: List[PurchaseOrderItemResponse] = []

    class Config:
        from_attributes = True
