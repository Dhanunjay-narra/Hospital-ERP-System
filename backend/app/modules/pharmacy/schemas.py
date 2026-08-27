from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class MedicineBatchCreate(BaseModel):
    batch_number: str
    expiry_date: date
    manufacturing_date: Optional[date] = None
    quantity_received: int = 100
    purchase_rate: float = 0.5
    selling_price: float = 1.0
    storage_location: Optional[str] = "Aisle 1 - Shelf A"

class MedicineBatchResponse(MedicineBatchCreate):
    id: str
    quantity_available: int
    created_at: datetime

    class Config:
        from_attributes = True

class MedicineBase(BaseModel):
    name: str
    generic_name: str
    sku_code: str
    category: str = "ANTIBIOTICS"
    dosage_form: str = "TABLET"
    strength: str = "500mg"
    manufacturer: Optional[str] = None
    unit_price: float = 1.0
    mrp: float = 1.5
    reorder_level: int = 100
    is_prescription_required: bool = True

class MedicineCreate(MedicineBase):
    batches: Optional[List[MedicineBatchCreate]] = []

class MedicineResponse(MedicineBase):
    id: str
    batches: List[MedicineBatchResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
