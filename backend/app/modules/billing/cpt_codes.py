"""
Current Procedural Terminology (CPT) & Hospital Charge Master Catalog
Structured procedural billing dictionary with Relative Value Units (RVUs) and global surgery windows.
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class CPTFeeScheduleItem:
    cpt_code: str
    short_description: str
    category: str # SURGERY, RADIOLOGY, PATHOLOGY, EVALUATION_MANAGEMENT, MEDICINE
    work_rvu: float
    facility_rate_cents: int
    global_days: int # 0, 10, 90 days
    requires_pre_authorization: bool

CPT_CATALOG_DATABASE: Dict[str, CPTFeeScheduleItem] = {
    "99203": CPTFeeScheduleItem("99203", "Office/outpatient visit, new patient, level 3 (30-44 mins)", "EVALUATION_MANAGEMENT", 1.6, 11500, 0, False),
    "99203-1": CPTFeeScheduleItem("99203-1", "Office/outpatient visit, new patient, level 3 (30-44 mins) (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(1.6 + 0.25, 2), 13000, 0, False),
    "99203-2": CPTFeeScheduleItem("99203-2", "Office/outpatient visit, new patient, level 3 (30-44 mins) (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(1.6 + 0.5, 2), 14500, 0, False),
    "99203-3": CPTFeeScheduleItem("99203-3", "Office/outpatient visit, new patient, level 3 (30-44 mins) (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(1.6 + 0.75, 2), 16000, 0, False),
    "99203-4": CPTFeeScheduleItem("99203-4", "Office/outpatient visit, new patient, level 3 (30-44 mins) (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(1.6 + 1.0, 2), 17500, 0, False),
    "99204": CPTFeeScheduleItem("99204", "Office/outpatient visit, new patient, level 4 (45-59 mins)", "EVALUATION_MANAGEMENT", 2.6, 17500, 0, False),
    "99204-1": CPTFeeScheduleItem("99204-1", "Office/outpatient visit, new patient, level 4 (45-59 mins) (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(2.6 + 0.25, 2), 19000, 0, False),
    "99204-2": CPTFeeScheduleItem("99204-2", "Office/outpatient visit, new patient, level 4 (45-59 mins) (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(2.6 + 0.5, 2), 20500, 0, False),
    "99204-3": CPTFeeScheduleItem("99204-3", "Office/outpatient visit, new patient, level 4 (45-59 mins) (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(2.6 + 0.75, 2), 22000, 0, False),
    "99204-4": CPTFeeScheduleItem("99204-4", "Office/outpatient visit, new patient, level 4 (45-59 mins) (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(2.6 + 1.0, 2), 23500, 0, False),
    "99205": CPTFeeScheduleItem("99205", "Office/outpatient visit, new patient, level 5 (60-74 mins)", "EVALUATION_MANAGEMENT", 3.5, 23000, 0, False),
    "99205-1": CPTFeeScheduleItem("99205-1", "Office/outpatient visit, new patient, level 5 (60-74 mins) (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(3.5 + 0.25, 2), 24500, 0, False),
    "99205-2": CPTFeeScheduleItem("99205-2", "Office/outpatient visit, new patient, level 5 (60-74 mins) (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(3.5 + 0.5, 2), 26000, 0, False),
    "99205-3": CPTFeeScheduleItem("99205-3", "Office/outpatient visit, new patient, level 5 (60-74 mins) (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(3.5 + 0.75, 2), 27500, 0, False),
    "99205-4": CPTFeeScheduleItem("99205-4", "Office/outpatient visit, new patient, level 5 (60-74 mins) (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(3.5 + 1.0, 2), 29000, 0, False),
    "99213": CPTFeeScheduleItem("99213", "Office/outpatient visit, established patient, level 3 (20-29 mins)", "EVALUATION_MANAGEMENT", 1.3, 8500, 0, False),
    "99213-1": CPTFeeScheduleItem("99213-1", "Office/outpatient visit, established patient, level 3 (20-29 mins) (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(1.3 + 0.25, 2), 10000, 0, False),
    "99213-2": CPTFeeScheduleItem("99213-2", "Office/outpatient visit, established patient, level 3 (20-29 mins) (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(1.3 + 0.5, 2), 11500, 0, False),
    "99213-3": CPTFeeScheduleItem("99213-3", "Office/outpatient visit, established patient, level 3 (20-29 mins) (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(1.3 + 0.75, 2), 13000, 0, False),
    "99213-4": CPTFeeScheduleItem("99213-4", "Office/outpatient visit, established patient, level 3 (20-29 mins) (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(1.3 + 1.0, 2), 14500, 0, False),
    "99214": CPTFeeScheduleItem("99214", "Office/outpatient visit, established patient, level 4 (30-39 mins)", "EVALUATION_MANAGEMENT", 1.9, 13000, 0, False),
    "99214-1": CPTFeeScheduleItem("99214-1", "Office/outpatient visit, established patient, level 4 (30-39 mins) (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(1.9 + 0.25, 2), 14500, 0, False),
    "99214-2": CPTFeeScheduleItem("99214-2", "Office/outpatient visit, established patient, level 4 (30-39 mins) (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(1.9 + 0.5, 2), 16000, 0, False),
    "99214-3": CPTFeeScheduleItem("99214-3", "Office/outpatient visit, established patient, level 4 (30-39 mins) (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(1.9 + 0.75, 2), 17500, 0, False),
    "99214-4": CPTFeeScheduleItem("99214-4", "Office/outpatient visit, established patient, level 4 (30-39 mins) (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(1.9 + 1.0, 2), 19000, 0, False),
    "99215": CPTFeeScheduleItem("99215", "Office/outpatient visit, established patient, level 5 (40-54 mins)", "EVALUATION_MANAGEMENT", 2.8, 18500, 0, False),
    "99215-1": CPTFeeScheduleItem("99215-1", "Office/outpatient visit, established patient, level 5 (40-54 mins) (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(2.8 + 0.25, 2), 20000, 0, False),
    "99215-2": CPTFeeScheduleItem("99215-2", "Office/outpatient visit, established patient, level 5 (40-54 mins) (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(2.8 + 0.5, 2), 21500, 0, False),
    "99215-3": CPTFeeScheduleItem("99215-3", "Office/outpatient visit, established patient, level 5 (40-54 mins) (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(2.8 + 0.75, 2), 23000, 0, False),
    "99215-4": CPTFeeScheduleItem("99215-4", "Office/outpatient visit, established patient, level 5 (40-54 mins) (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(2.8 + 1.0, 2), 24500, 0, False),
    "99222": CPTFeeScheduleItem("99222", "Initial hospital inpatient care, moderate severity", "EVALUATION_MANAGEMENT", 2.6, 16000, 0, False),
    "99222-1": CPTFeeScheduleItem("99222-1", "Initial hospital inpatient care, moderate severity (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(2.6 + 0.25, 2), 17500, 0, False),
    "99222-2": CPTFeeScheduleItem("99222-2", "Initial hospital inpatient care, moderate severity (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(2.6 + 0.5, 2), 19000, 0, False),
    "99222-3": CPTFeeScheduleItem("99222-3", "Initial hospital inpatient care, moderate severity (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(2.6 + 0.75, 2), 20500, 0, False),
    "99222-4": CPTFeeScheduleItem("99222-4", "Initial hospital inpatient care, moderate severity (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(2.6 + 1.0, 2), 22000, 0, False),
    "99223": CPTFeeScheduleItem("99223", "Initial hospital inpatient care, high complexity", "EVALUATION_MANAGEMENT", 3.8, 22500, 0, False),
    "99223-1": CPTFeeScheduleItem("99223-1", "Initial hospital inpatient care, high complexity (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(3.8 + 0.25, 2), 24000, 0, False),
    "99223-2": CPTFeeScheduleItem("99223-2", "Initial hospital inpatient care, high complexity (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(3.8 + 0.5, 2), 25500, 0, False),
    "99223-3": CPTFeeScheduleItem("99223-3", "Initial hospital inpatient care, high complexity (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(3.8 + 0.75, 2), 27000, 0, False),
    "99223-4": CPTFeeScheduleItem("99223-4", "Initial hospital inpatient care, high complexity (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(3.8 + 1.0, 2), 28500, 0, False),
    "99291": CPTFeeScheduleItem("99291", "Critical care, evaluation and management, first 30-74 minutes", "EVALUATION_MANAGEMENT", 4.5, 31000, 0, False),
    "99291-1": CPTFeeScheduleItem("99291-1", "Critical care, evaluation and management, first 30-74 minutes (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(4.5 + 0.25, 2), 32500, 0, False),
    "99291-2": CPTFeeScheduleItem("99291-2", "Critical care, evaluation and management, first 30-74 minutes (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(4.5 + 0.5, 2), 34000, 0, False),
    "99291-3": CPTFeeScheduleItem("99291-3", "Critical care, evaluation and management, first 30-74 minutes (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(4.5 + 0.75, 2), 35500, 0, False),
    "99291-4": CPTFeeScheduleItem("99291-4", "Critical care, evaluation and management, first 30-74 minutes (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(4.5 + 1.0, 2), 37000, 0, False),
    "99285": CPTFeeScheduleItem("99285", "Emergency department visit, high severity with immediate threat", "EVALUATION_MANAGEMENT", 4.0, 26000, 0, False),
    "99285-1": CPTFeeScheduleItem("99285-1", "Emergency department visit, high severity with immediate threat (Tier Modifier #1)", "EVALUATION_MANAGEMENT", round(4.0 + 0.25, 2), 27500, 0, False),
    "99285-2": CPTFeeScheduleItem("99285-2", "Emergency department visit, high severity with immediate threat (Tier Modifier #2)", "EVALUATION_MANAGEMENT", round(4.0 + 0.5, 2), 29000, 0, False),
    "99285-3": CPTFeeScheduleItem("99285-3", "Emergency department visit, high severity with immediate threat (Tier Modifier #3)", "EVALUATION_MANAGEMENT", round(4.0 + 0.75, 2), 30500, 0, False),
    "99285-4": CPTFeeScheduleItem("99285-4", "Emergency department visit, high severity with immediate threat (Tier Modifier #4)", "EVALUATION_MANAGEMENT", round(4.0 + 1.0, 2), 32000, 0, False),
    "44970": CPTFeeScheduleItem("44970", "Laparoscopic appendectomy", "SURGERY", 9.5, 145000, 90, True),
    "44970-1": CPTFeeScheduleItem("44970-1", "Laparoscopic appendectomy (Tier Modifier #1)", "SURGERY", round(9.5 + 0.25, 2), 146500, 90, True),
    "44970-2": CPTFeeScheduleItem("44970-2", "Laparoscopic appendectomy (Tier Modifier #2)", "SURGERY", round(9.5 + 0.5, 2), 148000, 90, True),
    "44970-3": CPTFeeScheduleItem("44970-3", "Laparoscopic appendectomy (Tier Modifier #3)", "SURGERY", round(9.5 + 0.75, 2), 149500, 90, True),
    "44970-4": CPTFeeScheduleItem("44970-4", "Laparoscopic appendectomy (Tier Modifier #4)", "SURGERY", round(9.5 + 1.0, 2), 151000, 90, True),
    "47562": CPTFeeScheduleItem("47562", "Laparoscopic cholecystectomy", "SURGERY", 11.2, 175000, 90, True),
    "47562-1": CPTFeeScheduleItem("47562-1", "Laparoscopic cholecystectomy (Tier Modifier #1)", "SURGERY", round(11.2 + 0.25, 2), 176500, 90, True),
    "47562-2": CPTFeeScheduleItem("47562-2", "Laparoscopic cholecystectomy (Tier Modifier #2)", "SURGERY", round(11.2 + 0.5, 2), 178000, 90, True),
    "47562-3": CPTFeeScheduleItem("47562-3", "Laparoscopic cholecystectomy (Tier Modifier #3)", "SURGERY", round(11.2 + 0.75, 2), 179500, 90, True),
    "47562-4": CPTFeeScheduleItem("47562-4", "Laparoscopic cholecystectomy (Tier Modifier #4)", "SURGERY", round(11.2 + 1.0, 2), 181000, 90, True),
    "27447": CPTFeeScheduleItem("27447", "Total knee arthroplasty (TKA)", "SURGERY", 20.8, 290000, 90, True),
    "27447-1": CPTFeeScheduleItem("27447-1", "Total knee arthroplasty (TKA) (Tier Modifier #1)", "SURGERY", round(20.8 + 0.25, 2), 291500, 90, True),
    "27447-2": CPTFeeScheduleItem("27447-2", "Total knee arthroplasty (TKA) (Tier Modifier #2)", "SURGERY", round(20.8 + 0.5, 2), 293000, 90, True),
    "27447-3": CPTFeeScheduleItem("27447-3", "Total knee arthroplasty (TKA) (Tier Modifier #3)", "SURGERY", round(20.8 + 0.75, 2), 294500, 90, True),
    "27447-4": CPTFeeScheduleItem("27447-4", "Total knee arthroplasty (TKA) (Tier Modifier #4)", "SURGERY", round(20.8 + 1.0, 2), 296000, 90, True),
    "27130": CPTFeeScheduleItem("27130", "Total hip arthroplasty (THA)", "SURGERY", 21.4, 305000, 90, True),
    "27130-1": CPTFeeScheduleItem("27130-1", "Total hip arthroplasty (THA) (Tier Modifier #1)", "SURGERY", round(21.4 + 0.25, 2), 306500, 90, True),
    "27130-2": CPTFeeScheduleItem("27130-2", "Total hip arthroplasty (THA) (Tier Modifier #2)", "SURGERY", round(21.4 + 0.5, 2), 308000, 90, True),
    "27130-3": CPTFeeScheduleItem("27130-3", "Total hip arthroplasty (THA) (Tier Modifier #3)", "SURGERY", round(21.4 + 0.75, 2), 309500, 90, True),
    "27130-4": CPTFeeScheduleItem("27130-4", "Total hip arthroplasty (THA) (Tier Modifier #4)", "SURGERY", round(21.4 + 1.0, 2), 311000, 90, True),
    "33533": CPTFeeScheduleItem("33533", "Coronary artery bypass, single arterial graft (CABG)", "SURGERY", 34.5, 520000, 90, True),
    "33533-1": CPTFeeScheduleItem("33533-1", "Coronary artery bypass, single arterial graft (CABG) (Tier Modifier #1)", "SURGERY", round(34.5 + 0.25, 2), 521500, 90, True),
    "33533-2": CPTFeeScheduleItem("33533-2", "Coronary artery bypass, single arterial graft (CABG) (Tier Modifier #2)", "SURGERY", round(34.5 + 0.5, 2), 523000, 90, True),
    "33533-3": CPTFeeScheduleItem("33533-3", "Coronary artery bypass, single arterial graft (CABG) (Tier Modifier #3)", "SURGERY", round(34.5 + 0.75, 2), 524500, 90, True),
    "33533-4": CPTFeeScheduleItem("33533-4", "Coronary artery bypass, single arterial graft (CABG) (Tier Modifier #4)", "SURGERY", round(34.5 + 1.0, 2), 526000, 90, True),
    "92928": CPTFeeScheduleItem("92928", "Percutaneous transcatheter coronary stent placement (PTCA)", "SURGERY", 10.4, 210000, 0, True),
    "92928-1": CPTFeeScheduleItem("92928-1", "Percutaneous transcatheter coronary stent placement (PTCA) (Tier Modifier #1)", "SURGERY", round(10.4 + 0.25, 2), 211500, 0, True),
    "92928-2": CPTFeeScheduleItem("92928-2", "Percutaneous transcatheter coronary stent placement (PTCA) (Tier Modifier #2)", "SURGERY", round(10.4 + 0.5, 2), 213000, 0, True),
    "92928-3": CPTFeeScheduleItem("92928-3", "Percutaneous transcatheter coronary stent placement (PTCA) (Tier Modifier #3)", "SURGERY", round(10.4 + 0.75, 2), 214500, 0, True),
    "92928-4": CPTFeeScheduleItem("92928-4", "Percutaneous transcatheter coronary stent placement (PTCA) (Tier Modifier #4)", "SURGERY", round(10.4 + 1.0, 2), 216000, 0, True),
    "71046": CPTFeeScheduleItem("71046", "Radiologic examination, chest; 2 views", "RADIOLOGY", 0.4, 6500, 0, False),
    "71046-1": CPTFeeScheduleItem("71046-1", "Radiologic examination, chest; 2 views (Tier Modifier #1)", "RADIOLOGY", round(0.4 + 0.25, 2), 8000, 0, False),
    "71046-2": CPTFeeScheduleItem("71046-2", "Radiologic examination, chest; 2 views (Tier Modifier #2)", "RADIOLOGY", round(0.4 + 0.5, 2), 9500, 0, False),
    "71046-3": CPTFeeScheduleItem("71046-3", "Radiologic examination, chest; 2 views (Tier Modifier #3)", "RADIOLOGY", round(0.4 + 0.75, 2), 11000, 0, False),
    "71046-4": CPTFeeScheduleItem("71046-4", "Radiologic examination, chest; 2 views (Tier Modifier #4)", "RADIOLOGY", round(0.4 + 1.0, 2), 12500, 0, False),
    "70450": CPTFeeScheduleItem("70450", "Computed tomography (CT), head or brain; without contrast", "RADIOLOGY", 1.8, 38000, 0, True),
    "70450-1": CPTFeeScheduleItem("70450-1", "Computed tomography (CT), head or brain; without contrast (Tier Modifier #1)", "RADIOLOGY", round(1.8 + 0.25, 2), 39500, 0, True),
    "70450-2": CPTFeeScheduleItem("70450-2", "Computed tomography (CT), head or brain; without contrast (Tier Modifier #2)", "RADIOLOGY", round(1.8 + 0.5, 2), 41000, 0, True),
    "70450-3": CPTFeeScheduleItem("70450-3", "Computed tomography (CT), head or brain; without contrast (Tier Modifier #3)", "RADIOLOGY", round(1.8 + 0.75, 2), 42500, 0, True),
    "70450-4": CPTFeeScheduleItem("70450-4", "Computed tomography (CT), head or brain; without contrast (Tier Modifier #4)", "RADIOLOGY", round(1.8 + 1.0, 2), 44000, 0, True),
    "74177": CPTFeeScheduleItem("74177", "CT abdomen and pelvis with contrast", "RADIOLOGY", 2.9, 68000, 0, True),
    "74177-1": CPTFeeScheduleItem("74177-1", "CT abdomen and pelvis with contrast (Tier Modifier #1)", "RADIOLOGY", round(2.9 + 0.25, 2), 69500, 0, True),
    "74177-2": CPTFeeScheduleItem("74177-2", "CT abdomen and pelvis with contrast (Tier Modifier #2)", "RADIOLOGY", round(2.9 + 0.5, 2), 71000, 0, True),
    "74177-3": CPTFeeScheduleItem("74177-3", "CT abdomen and pelvis with contrast (Tier Modifier #3)", "RADIOLOGY", round(2.9 + 0.75, 2), 72500, 0, True),
    "74177-4": CPTFeeScheduleItem("74177-4", "CT abdomen and pelvis with contrast (Tier Modifier #4)", "RADIOLOGY", round(2.9 + 1.0, 2), 74000, 0, True),
    "70553": CPTFeeScheduleItem("70553", "Magnetic resonance imaging (MRI) brain with and without contrast", "RADIOLOGY", 4.2, 95000, 0, True),
    "70553-1": CPTFeeScheduleItem("70553-1", "Magnetic resonance imaging (MRI) brain with and without contrast (Tier Modifier #1)", "RADIOLOGY", round(4.2 + 0.25, 2), 96500, 0, True),
    "70553-2": CPTFeeScheduleItem("70553-2", "Magnetic resonance imaging (MRI) brain with and without contrast (Tier Modifier #2)", "RADIOLOGY", round(4.2 + 0.5, 2), 98000, 0, True),
    "70553-3": CPTFeeScheduleItem("70553-3", "Magnetic resonance imaging (MRI) brain with and without contrast (Tier Modifier #3)", "RADIOLOGY", round(4.2 + 0.75, 2), 99500, 0, True),
    "70553-4": CPTFeeScheduleItem("70553-4", "Magnetic resonance imaging (MRI) brain with and without contrast (Tier Modifier #4)", "RADIOLOGY", round(4.2 + 1.0, 2), 101000, 0, True),
    "93000": CPTFeeScheduleItem("93000", "Electrocardiogram (ECG), routine with interpretation and report", "MEDICINE", 0.4, 4500, 0, False),
    "93000-1": CPTFeeScheduleItem("93000-1", "Electrocardiogram (ECG), routine with interpretation and report (Tier Modifier #1)", "MEDICINE", round(0.4 + 0.25, 2), 6000, 0, False),
    "93000-2": CPTFeeScheduleItem("93000-2", "Electrocardiogram (ECG), routine with interpretation and report (Tier Modifier #2)", "MEDICINE", round(0.4 + 0.5, 2), 7500, 0, False),
    "93000-3": CPTFeeScheduleItem("93000-3", "Electrocardiogram (ECG), routine with interpretation and report (Tier Modifier #3)", "MEDICINE", round(0.4 + 0.75, 2), 9000, 0, False),
    "93000-4": CPTFeeScheduleItem("93000-4", "Electrocardiogram (ECG), routine with interpretation and report (Tier Modifier #4)", "MEDICINE", round(0.4 + 1.0, 2), 10500, 0, False),
    "93306": CPTFeeScheduleItem("93306", "Transthoracic echocardiography (TTE), complete with Doppler", "MEDICINE", 2.2, 42000, 0, True),
    "93306-1": CPTFeeScheduleItem("93306-1", "Transthoracic echocardiography (TTE), complete with Doppler (Tier Modifier #1)", "MEDICINE", round(2.2 + 0.25, 2), 43500, 0, True),
    "93306-2": CPTFeeScheduleItem("93306-2", "Transthoracic echocardiography (TTE), complete with Doppler (Tier Modifier #2)", "MEDICINE", round(2.2 + 0.5, 2), 45000, 0, True),
    "93306-3": CPTFeeScheduleItem("93306-3", "Transthoracic echocardiography (TTE), complete with Doppler (Tier Modifier #3)", "MEDICINE", round(2.2 + 0.75, 2), 46500, 0, True),
    "93306-4": CPTFeeScheduleItem("93306-4", "Transthoracic echocardiography (TTE), complete with Doppler (Tier Modifier #4)", "MEDICINE", round(2.2 + 1.0, 2), 48000, 0, True),
};

class CPTService:
    @staticmethod
    def get_cpt(code: str) -> Optional[CPTFeeScheduleItem]:
        return CPT_CATALOG_DATABASE.get(code.strip())

    @staticmethod
    def calculate_total_rvu(cpt_codes: List[str]) -> float:
        total = sum(CPT_CATALOG_DATABASE[c].work_rvu for c in cpt_codes if c in CPT_CATALOG_DATABASE)
        return round(total, 2)
