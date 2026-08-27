from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.inventory.models import InventoryWarehouse, InventoryItem
from app.modules.inventory.schemas import InventoryWarehouseCreate, InventoryItemCreate
from app.core.exceptions import NotFoundError, ConflictError

class InventoryService:
    @staticmethod
    def get_warehouses(db: Session) -> List[InventoryWarehouse]:
        return db.query(InventoryWarehouse).all()

    @staticmethod
    def create_warehouse(db: Session, wh_in: InventoryWarehouseCreate) -> InventoryWarehouse:
        existing = db.query(InventoryWarehouse).filter(InventoryWarehouse.code == wh_in.code).first()
        if existing:
            return existing
        wh = InventoryWarehouse(**wh_in.model_dump())
        db.add(wh)
        db.commit()
        db.refresh(wh)
        return wh

    @staticmethod
    def get_items(db: Session, skip: int = 0, limit: int = 20, warehouse_id: Optional[str] = None, category: Optional[str] = None) -> Tuple[List[InventoryItem], int]:
        query = db.query(InventoryItem)
        if warehouse_id:
            query = query.filter(InventoryItem.warehouse_id == warehouse_id)
        if category:
            query = query.filter(InventoryItem.category == category)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    @staticmethod
    def create_item(db: Session, item_in: InventoryItemCreate, created_by: Optional[str] = None) -> InventoryItem:
        existing = db.query(InventoryItem).filter(InventoryItem.item_code == item_in.item_code).first()
        if existing:
            return existing
        item = InventoryItem(**item_in.model_dump(), created_by=created_by)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
