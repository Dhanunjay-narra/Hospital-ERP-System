from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class MARBase(BaseModel):
    admission_id: str
    prescription_item_id: Optional[str] = None
    medicine_name: str
    dosage: str
    route: str = "ORAL"
    scheduled_time: datetime

class MARCreate(MARBase):
    pass

class MARAdministerRequest(BaseModel):
    status: str = "GIVEN" # GIVEN, MISSED, REFUSED, HELD
    notes: Optional[str] = None

class MARResponse(MARBase):
    id: str
    administered_time: Optional[datetime] = None
    administered_by_nurse_id: Optional[str] = None
    status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class NursingNoteCreate(BaseModel):
    admission_id: str
    shift_type: str = "DAY"
    observations: str
    interventions: Optional[str] = None
    patient_response: Optional[str] = None
    handover_instructions: Optional[str] = None

class NursingNoteResponse(NursingNoteCreate):
    id: str
    nurse_id: str
    note_datetime: datetime

    class Config:
        from_attributes = True

class IntakeOutputChartCreate(BaseModel):
    admission_id: str
    oral_intake_ml: float = 0.0
    iv_fluids_ml: float = 0.0
    ng_tube_ml: float = 0.0
    urine_output_ml: float = 0.0
    drain_output_ml: float = 0.0
    vomitus_ml: float = 0.0
    stool_count: int = 0

class IntakeOutputChartResponse(IntakeOutputChartCreate):
    id: str
    total_intake_ml: float
    total_output_ml: float
    balance_ml: float
    recorded_at: datetime

    class Config:
        from_attributes = True
