from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.billing.models import Invoice, InvoiceItem, PaymentTransaction
from app.modules.billing.schemas import InvoiceCreate, PaymentTransactionCreate
from app.core.exceptions import NotFoundError, AppException
from app.core.events import event_bus

class BillingService:
    @staticmethod
    def get_invoices(db: Session, skip: int = 0, limit: int = 20, patient_id: Optional[str] = None, status: Optional[str] = None) -> Tuple[List[Invoice], int]:
        query = db.query(Invoice)
        if patient_id:
            query = query.filter(Invoice.patient_id == patient_id)
        if status:
            query = query.filter(Invoice.status == status)
        total = query.count()
        invoices = query.order_by(Invoice.invoice_date.desc()).offset(skip).limit(limit).all()
        return invoices, total

    @staticmethod
    def create_invoice(db: Session, inv_in: InvoiceCreate, created_by: Optional[str] = None) -> Invoice:
        count = db.query(Invoice).count() + 1
        inv_num = f"INV-{datetime.utcnow().year}-{count:05d}"

        subtotal = 0.0
        tax_total = 0.0
        discount_total = 0.0

        for item_data in inv_in.items:
            item_sub = item_data.unit_price * item_data.quantity
            disc = item_sub * (item_data.discount_percent / 100.0)
            item_total = item_sub - disc + item_data.tax_amount
            subtotal += item_sub
            discount_total += disc
            tax_total += item_data.tax_amount

        grand_total = subtotal - discount_total + tax_total

        invoice = Invoice(
            invoice_number=inv_num,
            patient_id=inv_in.patient_id,
            admission_id=inv_in.admission_id,
            opd_visit_id=inv_in.opd_visit_id,
            subtotal=subtotal,
            discount_amount=discount_total,
            tax_amount=tax_total,
            total_amount=grand_total,
            paid_amount=0.0,
            balance_amount=grand_total,
            status="ISSUED",
            created_by=created_by
        )
        db.add(invoice)
        db.flush()

        for item_data in inv_in.items:
            item_sub = item_data.unit_price * item_data.quantity
            disc = item_sub * (item_data.discount_percent / 100.0)
            item_total = item_sub - disc + item_data.tax_amount

            item = InvoiceItem(
                invoice_id=invoice.id,
                service_name=item_data.service_name,
                service_code=item_data.service_code,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                discount_percent=item_data.discount_percent,
                tax_amount=item_data.tax_amount,
                total_price=item_total
            )
            db.add(item)

        db.commit()
        db.refresh(invoice)

        event_bus.publish("billing.invoice_created", {
            "invoice_id": invoice.id,
            "patient_id": invoice.patient_id,
            "total_amount": invoice.total_amount
        })

        return invoice

    @staticmethod
    def record_payment(db: Session, pay_in: PaymentTransactionCreate, cashier_id: Optional[str] = None) -> PaymentTransaction:
        inv = db.query(Invoice).filter(Invoice.id == pay_in.invoice_id).first()
        if not inv:
            raise NotFoundError("Invoice not found")

        count = db.query(PaymentTransaction).count() + 1
        rec_num = f"REC-{datetime.utcnow().year}-{count:05d}"

        payment = PaymentTransaction(
            receipt_number=rec_num,
            invoice_id=inv.id,
            patient_id=inv.patient_id,
            amount=pay_in.amount,
            payment_method=pay_in.payment_method,
            transaction_reference=pay_in.transaction_reference,
            notes=pay_in.notes,
            cashier_id=cashier_id
        )
        db.add(payment)

        inv.paid_amount += pay_in.amount
        inv.balance_amount = max(0.0, inv.total_amount - inv.paid_amount)
        if inv.balance_amount == 0:
            inv.status = "PAID"
        else:
            inv.status = "PARTIALLY_PAID"

        db.commit()
        db.refresh(payment)

        event_bus.publish("billing.payment_received", {
            "receipt_number": rec_num,
            "invoice_id": inv.id,
            "amount": pay_in.amount
        })

        return payment
