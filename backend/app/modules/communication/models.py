import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class CommunicationTemplate(BaseModel):
    __tablename__ = "communication_templates"

    template_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. TPL-APPT-CONFIRM, TPL-DISCHARGE-CARE
    title = Column(String(150), nullable=False)
    channel = Column(String(30), default="SMS", nullable=False) # SMS, WHATSAPP, EMAIL
    body_content = Column(Text, nullable=False) # "Dear {{patient_name}}, your appointment with {{doctor_name}} is confirmed for {{time}}."
    is_active_template = Column(Boolean, default=True, nullable=False)

class DispatchedMessage(BaseModel):
    __tablename__ = "dispatched_messages"

    recipient_phone = Column(String(50), nullable=True)
    recipient_email = Column(String(255), nullable=True)
    patient_id = Column(String(36), ForeignKey("patients.id", ondelete="SET NULL"), nullable=True)
    
    channel = Column(String(30), default="SMS", nullable=False) # SMS, WHATSAPP, EMAIL
    message_subject = Column(String(200), nullable=True)
    message_body = Column(Text, nullable=False)
    
    # STATUS: QUEUED, SENT, DELIVERED, FAILED
    status = Column(String(30), default="SENT", index=True, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("Patient", lazy="joined")
