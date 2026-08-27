from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class CommunicationTemplateBase(BaseModel):
    template_code: str
    title: str
    channel: str = "SMS" # SMS, WHATSAPP, EMAIL
    body_content: str
    is_active_template: bool = True

class CommunicationTemplateCreate(CommunicationTemplateBase):
    pass

class CommunicationTemplateResponse(CommunicationTemplateBase):
    id: str

    class Config:
        from_attributes = True

class DispatchedMessageCreate(BaseModel):
    recipient_phone: Optional[str] = None
    recipient_email: Optional[str] = None
    patient_id: Optional[str] = None
    channel: str = "SMS"
    message_subject: Optional[str] = None
    message_body: str

class DispatchedMessageResponse(DispatchedMessageCreate):
    id: str
    status: str
    sent_at: datetime

    class Config:
        from_attributes = True
