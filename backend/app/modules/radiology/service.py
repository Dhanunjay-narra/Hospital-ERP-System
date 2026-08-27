from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.radiology.models import RadiologyOrder
from app.modules.radiology.schemas import RadiologyOrderCreate, RadiologyReportSubmit
from app.core.exceptions import NotFoundError
from app.core.events import event_bus

class RadiologyService:
    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 20, modality: Optional[str] = None, status: Optional[str] = None) -> Tuple[List[RadiologyOrder], int]:
        query = db.query(RadiologyOrder)
        if modality:
            query = query.filter(RadiologyOrder.modality == modality)
        if status:
            query = query.filter(RadiologyOrder.status == status)
        total = query.count()
        orders = query.order_by(RadiologyOrder.created_at.desc()).offset(skip).limit(limit).all()
        return orders, total

    @staticmethod
    def create_order(db: Session, order_in: RadiologyOrderCreate, created_by: Optional[str] = None) -> RadiologyOrder:
        count = db.query(RadiologyOrder).count() + 1
        order = RadiologyOrder(
            order_number=f"RAD-{datetime.utcnow().year}-{count:05d}",
            status="ORDERED",
            **order_in.model_dump(),
            created_by=created_by
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def submit_report(db: Session, order_id: str, report_in: RadiologyReportSubmit, radiologist_id: str) -> RadiologyOrder:
        order = db.query(RadiologyOrder).filter(RadiologyOrder.id == order_id).first()
        if not order:
            raise NotFoundError("Radiology order not found")

        order.status = "REPORTED"
        order.radiologist_id = radiologist_id
        order.radiology_findings = report_in.radiology_findings
        order.impression = report_in.impression
        order.is_critical_finding = report_in.is_critical_finding
        order.pacs_image_url = report_in.pacs_image_url
        order.reported_at = datetime.utcnow()

        db.commit()
        db.refresh(order)

        if report_in.is_critical_finding:
            event_bus.publish("radiology.critical_finding_alert", {
                "order_id": order.id,
                "impression": order.impression
            })

        return order
