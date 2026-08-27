from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.procurement.models import Vendor, PurchaseOrder, PurchaseOrderItem
from app.modules.procurement.schemas import VendorCreate, PurchaseOrderCreate
from app.core.exceptions import NotFoundError, ConflictError
from app.core.events import event_bus

class ProcurementService:
    @staticmethod
    def get_vendors(db: Session) -> List[Vendor]:
        return db.query(Vendor).all()

    @staticmethod
    def create_vendor(db: Session, ven_in: VendorCreate) -> Vendor:
        existing = db.query(Vendor).filter(Vendor.vendor_code == ven_in.vendor_code).first()
        if existing:
            return existing
        ven = Vendor(**ven_in.model_dump())
        db.add(ven)
        db.commit()
        db.refresh(ven)
        return ven

    @staticmethod
    def get_purchase_orders(db: Session, skip: int = 0, limit: int = 20, vendor_id: Optional[str] = None, status: Optional[str] = None) -> Tuple[List[PurchaseOrder], int]:
        query = db.query(PurchaseOrder)
        if vendor_id:
            query = query.filter(PurchaseOrder.vendor_id == vendor_id)
        if status:
            query = query.filter(PurchaseOrder.status == status)
        total = query.count()
        pos = query.order_by(PurchaseOrder.order_date.desc()).offset(skip).limit(limit).all()
        return pos, total

    @staticmethod
    def create_purchase_order(db: Session, po_in: PurchaseOrderCreate, created_by: Optional[str] = None) -> PurchaseOrder:
        count = db.query(PurchaseOrder).count() + 1
        po_num = f"PO-{datetime.utcnow().year}-{count:05d}"

        subtotal = 0.0
        for it in po_in.items:
            subtotal += it.unit_price * it.quantity_ordered
        tax = subtotal * 0.05
        grand = subtotal + tax

        po = PurchaseOrder(
            po_number=po_num,
            vendor_id=po_in.vendor_id,
            warehouse_id=po_in.warehouse_id,
            expected_delivery_date=po_in.expected_delivery_date,
            total_amount=subtotal,
            tax_amount=tax,
            grand_total=grand,
            status="SUBMITTED",
            created_by=created_by
        )
        db.add(po)
        db.flush()

        for it in po_in.items:
            item_total = it.unit_price * it.quantity_ordered
            po_item = PurchaseOrderItem(
                po_id=po.id,
                item_id=it.item_id,
                item_name=it.item_name,
                quantity_ordered=it.quantity_ordered,
                unit_price=it.unit_price,
                total_price=item_total
            )
            db.add(po_item)

        db.commit()
        db.refresh(po)

        event_bus.publish("procurement.po_created", {
            "po_id": po.id,
            "vendor_id": po.vendor_id,
            "grand_total": po.grand_total
        })

        return po
