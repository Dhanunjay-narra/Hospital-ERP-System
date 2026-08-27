from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class InventoryWarehouseBase(BaseModel):
    name: str
    code: str
    location: Optional[str] = "Main Building - Level B1"

class InventoryWarehouseCreate(InventoryWarehouseBase):
    pass

class InventoryWarehouseResponse(InventoryWarehouseBase):
    id: str

    class Config:
        from_attributes = True

class InventoryItemBase(BaseModel):
    item_code: str
    item_name: str
    category: str = "CONSUMABLES" # CONSUMABLES, SURGICAL_INSTRUMENTS, LINEN, PPE
    unit_of_measure: str = "BOX"
    warehouse_id: str
    quantity_on_hand: int = 0
    reorder_threshold: int = 50
    unit_cost: float = 1.0

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemResponse(InventoryItemBase):
    id: str
    warehouse: Optional[InventoryWarehouseResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
