from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.modules.patients.schemas import PatientResponse
from app.modules.doctors.schemas import DoctorResponse

class LabTestCatalogBase(BaseModel):
    test_code: str
    test_name: str
    department: str = "HEMATOLOGY"
    sample_type: str = "WHOLE_BLOOD"
    turnaround_time_hours: int = 4
    price: float = 50.0
    unit_of_measure: Optional[str] = None
    reference_min: Optional[float] = None
    reference_max: Optional[float] = None
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None

class LabTestCatalogCreate(LabTestCatalogBase):
    pass

class LabTestCatalogResponse(LabTestCatalogBase):
    id: str

    class Config:
        from_attributes = True

class LabResultBase(BaseModel):
    test_id: str
    parameter_name: str
    result_value: str
    numeric_value: Optional[float] = None
    unit_of_measure: Optional[str] = None
    reference_range: Optional[str] = None
    is_abnormal: bool = False
    is_critical: bool = False
    technician_remarks: Optional[str] = None

class LabResultCreate(LabResultBase):
    pass

class LabResultResponse(LabResultBase):
    id: str

    class Config:
        from_attributes = True

class LabOrderCreate(BaseModel):
    patient_id: str
    doctor_id: str
    admission_id: Optional[str] = None
    opd_visit_id: Optional[str] = None
    priority: str = "ROUTINE"
    test_ids: List[str]

class LabOrderResponse(BaseModel):
    id: str
    order_number: str
    priority: str
    status: str
    sample_barcode: Optional[str] = None
    order_datetime: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    results: List[LabResultResponse] = []

    class Config:
        from_attributes = True
