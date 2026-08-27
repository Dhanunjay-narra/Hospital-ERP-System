from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.inventory.schemas import (
    InventoryWarehouseCreate, InventoryWarehouseResponse,
    InventoryItemCreate, InventoryItemResponse
)
from app.modules.inventory.service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory & Stores"])

@router.get("/warehouses", response_model=List[InventoryWarehouseResponse])
def list_warehouses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InventoryService.get_warehouses(db)

@router.post("/warehouses", response_model=InventoryWarehouseResponse)
def create_warehouse(
    wh_in: InventoryWarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "INVENTORY_MANAGER"))
):
    return InventoryService.create_warehouse(db, wh_in)

@router.get("/items", response_model=PaginatedResponse[InventoryItemResponse])
def list_inventory_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    warehouse_id: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    items, total = InventoryService.get_items(db, skip=params.skip, limit=params.limit, warehouse_id=warehouse_id, category=category)
    return PaginatedResponse.create(items=items, total=total, params=params)

@router.post("/items", response_model=InventoryItemResponse)
def create_inventory_item(
    item_in: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "INVENTORY_MANAGER"))
):
    return InventoryService.create_item(db, item_in, created_by=current_user.id)
