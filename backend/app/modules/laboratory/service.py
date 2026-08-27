from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.laboratory.models import LabTestCatalog, LabOrder, LabResult
from app.modules.laboratory.schemas import LabTestCatalogCreate, LabOrderCreate, LabResultCreate
from app.core.exceptions import NotFoundError
from app.core.events import event_bus

class LabService:
    @staticmethod
    def get_catalog(db: Session) -> List[LabTestCatalog]:
        return db.query(LabTestCatalog).all()

    @staticmethod
    def create_test(db: Session, test_in: LabTestCatalogCreate) -> LabTestCatalog:
        test = LabTestCatalog(**test_in.model_dump())
        db.add(test)
        db.commit()
        db.refresh(test)
        return test

    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 20, patient_id: Optional[str] = None, status: Optional[str] = None) -> Tuple[List[LabOrder], int]:
        query = db.query(LabOrder)
        if patient_id:
            query = query.filter(LabOrder.patient_id == patient_id)
        if status:
            query = query.filter(LabOrder.status == status)
        total = query.count()
        orders = query.order_by(LabOrder.order_datetime.desc()).offset(skip).limit(limit).all()
        return orders, total

    @staticmethod
    def create_order(db: Session, order_in: LabOrderCreate, created_by: Optional[str] = None) -> LabOrder:
        count = db.query(LabOrder).count() + 1
        order = LabOrder(
            order_number=f"LAB-{datetime.utcnow().year}-{count:05d}",
            patient_id=order_in.patient_id,
            doctor_id=order_in.doctor_id,
            admission_id=order_in.admission_id,
            opd_visit_id=order_in.opd_visit_id,
            priority=order_in.priority,
            sample_barcode=f"BAR-LAB-{count:06d}",
            status="ORDERED",
            created_by=created_by
        )
        db.add(order)
        db.flush()

        for t_id in order_in.test_ids:
            catalog_item = db.query(LabTestCatalog).filter(LabTestCatalog.id == t_id).first()
            if catalog_item:
                result = LabResult(
                    lab_order_id=order.id,
                    test_id=catalog_item.id,
                    parameter_name=catalog_item.test_name,
                    result_value="Pending",
                    unit_of_measure=catalog_item.unit_of_measure,
                    reference_range=f"{catalog_item.reference_min} - {catalog_item.reference_max}" if catalog_item.reference_min else "Normal"
                )
                db.add(result)

        db.commit()
        db.refresh(order)

        event_bus.publish("laboratory.order_created", {
            "order_id": order.id,
            "patient_id": order.patient_id,
            "priority": order.priority
        })

        return order

    @staticmethod
    def enter_result(db: Session, result_id: str, value: str, numeric_val: Optional[float] = None) -> LabResult:
        res = db.query(LabResult).filter(LabResult.id == result_id).first()
        if not res:
            raise NotFoundError("Lab Result item not found")

        res.result_value = value
        res.numeric_value = numeric_val

        # Auto-evaluate abnormality and critical panic status
        test = res.test
        if numeric_val is not None and test:
            if test.reference_min is not None and numeric_val < test.reference_min:
                res.is_abnormal = True
            elif test.reference_max is not None and numeric_val > test.reference_max:
                res.is_abnormal = True
            
            if test.critical_low is not None and numeric_val <= test.critical_low:
                res.is_critical = True
            elif test.critical_high is not None and numeric_val >= test.critical_high:
                res.is_critical = True

        res.order.status = "RESULTED"
        db.commit()
        db.refresh(res)

        if res.is_critical:
            event_bus.publish("laboratory.critical_panic_alert", {
                "order_id": res.lab_order_id,
                "parameter": res.parameter_name,
                "value": res.result_value
            })

        return res
