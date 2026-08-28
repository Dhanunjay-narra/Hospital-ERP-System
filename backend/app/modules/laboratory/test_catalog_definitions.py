"""
Standardized Clinical Diagnostic & Pathology Test Catalog
Defines reference biological intervals, specimen tubes, critical panic limits, and delta checks.
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LabTestProfile:
    test_code: str
    test_name: str
    discipline: str # BIOCHEMISTRY, HEMATOLOGY, MICROBIOLOGY, IMMUNOLOGY, HISTOPATHOLOGY
    specimen_type: str # SERUM, WHOLE_BLOOD_EDTA, CITRATE_PLASMA, URINE, CSF
    tube_color: str # GOLD_SST, LAVENDER_EDTA, LIGHT_BLUE_CITRATE, RED_SERUM, GREEN_HEPARIN
    units: str
    reference_low: float
    reference_high: float
    critical_panic_low: Optional[float]
    critical_panic_high: Optional[float]
    turnaround_time_mins: int
    cost_cents: int

LAB_CATALOG_DATABASE: Dict[str, LabTestProfile] = {
    "LAB-HEM-CBC-WBC": LabTestProfile("LAB-HEM-CBC-WBC", "White Blood Cell Count (WBC)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 4.5, 11.0, 2.0, 30.0, 45, 1800),
    "LAB-HEM-CBC-WBC-SUB1": LabTestProfile("LAB-HEM-CBC-WBC-SUB1", "White Blood Cell Count (WBC) (Assay Variant #1)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 4.5, 11.0, 2.0, 30.0, 45, 1800),
    "LAB-HEM-CBC-WBC-SUB2": LabTestProfile("LAB-HEM-CBC-WBC-SUB2", "White Blood Cell Count (WBC) (Assay Variant #2)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 4.5, 11.0, 2.0, 30.0, 45, 1800),
    "LAB-HEM-CBC-WBC-SUB3": LabTestProfile("LAB-HEM-CBC-WBC-SUB3", "White Blood Cell Count (WBC) (Assay Variant #3)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 4.5, 11.0, 2.0, 30.0, 45, 1800),
    "LAB-HEM-CBC-WBC-SUB4": LabTestProfile("LAB-HEM-CBC-WBC-SUB4", "White Blood Cell Count (WBC) (Assay Variant #4)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 4.5, 11.0, 2.0, 30.0, 45, 1800),
    "LAB-HEM-CBC-HGB": LabTestProfile("LAB-HEM-CBC-HGB", "Hemoglobin (Hgb)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "g/dL", 13.5, 17.5, 7.0, 20.0, 45, 1800),
    "LAB-HEM-CBC-HGB-SUB1": LabTestProfile("LAB-HEM-CBC-HGB-SUB1", "Hemoglobin (Hgb) (Assay Variant #1)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "g/dL", 13.5, 17.5, 7.0, 20.0, 45, 1800),
    "LAB-HEM-CBC-HGB-SUB2": LabTestProfile("LAB-HEM-CBC-HGB-SUB2", "Hemoglobin (Hgb) (Assay Variant #2)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "g/dL", 13.5, 17.5, 7.0, 20.0, 45, 1800),
    "LAB-HEM-CBC-HGB-SUB3": LabTestProfile("LAB-HEM-CBC-HGB-SUB3", "Hemoglobin (Hgb) (Assay Variant #3)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "g/dL", 13.5, 17.5, 7.0, 20.0, 45, 1800),
    "LAB-HEM-CBC-HGB-SUB4": LabTestProfile("LAB-HEM-CBC-HGB-SUB4", "Hemoglobin (Hgb) (Assay Variant #4)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "g/dL", 13.5, 17.5, 7.0, 20.0, 45, 1800),
    "LAB-HEM-CBC-PLT": LabTestProfile("LAB-HEM-CBC-PLT", "Platelet Count", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 150.0, 450.0, 40.0, 1000.0, 45, 1800),
    "LAB-HEM-CBC-PLT-SUB1": LabTestProfile("LAB-HEM-CBC-PLT-SUB1", "Platelet Count (Assay Variant #1)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 150.0, 450.0, 40.0, 1000.0, 45, 1800),
    "LAB-HEM-CBC-PLT-SUB2": LabTestProfile("LAB-HEM-CBC-PLT-SUB2", "Platelet Count (Assay Variant #2)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 150.0, 450.0, 40.0, 1000.0, 45, 1800),
    "LAB-HEM-CBC-PLT-SUB3": LabTestProfile("LAB-HEM-CBC-PLT-SUB3", "Platelet Count (Assay Variant #3)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 150.0, 450.0, 40.0, 1000.0, 45, 1800),
    "LAB-HEM-CBC-PLT-SUB4": LabTestProfile("LAB-HEM-CBC-PLT-SUB4", "Platelet Count (Assay Variant #4)", "HEMATOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "10^3/uL", 150.0, 450.0, 40.0, 1000.0, 45, 1800),
    "LAB-COAG-PT-INR": LabTestProfile("LAB-COAG-PT-INR", "Prothrombin Time & INR", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "INR Ratio", 0.9, 1.15, None, 4.5, 60, 2500),
    "LAB-COAG-PT-INR-SUB1": LabTestProfile("LAB-COAG-PT-INR-SUB1", "Prothrombin Time & INR (Assay Variant #1)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "INR Ratio", 0.9, 1.15, None, 4.5, 60, 2500),
    "LAB-COAG-PT-INR-SUB2": LabTestProfile("LAB-COAG-PT-INR-SUB2", "Prothrombin Time & INR (Assay Variant #2)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "INR Ratio", 0.9, 1.15, None, 4.5, 60, 2500),
    "LAB-COAG-PT-INR-SUB3": LabTestProfile("LAB-COAG-PT-INR-SUB3", "Prothrombin Time & INR (Assay Variant #3)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "INR Ratio", 0.9, 1.15, None, 4.5, 60, 2500),
    "LAB-COAG-PT-INR-SUB4": LabTestProfile("LAB-COAG-PT-INR-SUB4", "Prothrombin Time & INR (Assay Variant #4)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "INR Ratio", 0.9, 1.15, None, 4.5, 60, 2500),
    "LAB-COAG-APTT": LabTestProfile("LAB-COAG-APTT", "Activated Partial Thromboplastin Time", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "Seconds", 25.0, 35.0, None, 80.0, 60, 2500),
    "LAB-COAG-APTT-SUB1": LabTestProfile("LAB-COAG-APTT-SUB1", "Activated Partial Thromboplastin Time (Assay Variant #1)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "Seconds", 25.0, 35.0, None, 80.0, 60, 2500),
    "LAB-COAG-APTT-SUB2": LabTestProfile("LAB-COAG-APTT-SUB2", "Activated Partial Thromboplastin Time (Assay Variant #2)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "Seconds", 25.0, 35.0, None, 80.0, 60, 2500),
    "LAB-COAG-APTT-SUB3": LabTestProfile("LAB-COAG-APTT-SUB3", "Activated Partial Thromboplastin Time (Assay Variant #3)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "Seconds", 25.0, 35.0, None, 80.0, 60, 2500),
    "LAB-COAG-APTT-SUB4": LabTestProfile("LAB-COAG-APTT-SUB4", "Activated Partial Thromboplastin Time (Assay Variant #4)", "HEMATOLOGY", "CITRATE_PLASMA", "LIGHT_BLUE_CITRATE", "Seconds", 25.0, 35.0, None, 80.0, 60, 2500),
    "LAB-CHM-GLUC": LabTestProfile("LAB-CHM-GLUC", "Fasting Plasma Glucose", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 70.0, 99.0, 45.0, 450.0, 60, 1200),
    "LAB-CHM-GLUC-SUB1": LabTestProfile("LAB-CHM-GLUC-SUB1", "Fasting Plasma Glucose (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 70.0, 99.0, 45.0, 450.0, 60, 1200),
    "LAB-CHM-GLUC-SUB2": LabTestProfile("LAB-CHM-GLUC-SUB2", "Fasting Plasma Glucose (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 70.0, 99.0, 45.0, 450.0, 60, 1200),
    "LAB-CHM-GLUC-SUB3": LabTestProfile("LAB-CHM-GLUC-SUB3", "Fasting Plasma Glucose (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 70.0, 99.0, 45.0, 450.0, 60, 1200),
    "LAB-CHM-GLUC-SUB4": LabTestProfile("LAB-CHM-GLUC-SUB4", "Fasting Plasma Glucose (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 70.0, 99.0, 45.0, 450.0, 60, 1200),
    "LAB-CHM-HBA1C": LabTestProfile("LAB-CHM-HBA1C", "Glycated Hemoglobin (HbA1c)", "BIOCHEMISTRY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "%", 4.0, 5.6, None, 13.0, 120, 3500),
    "LAB-CHM-HBA1C-SUB1": LabTestProfile("LAB-CHM-HBA1C-SUB1", "Glycated Hemoglobin (HbA1c) (Assay Variant #1)", "BIOCHEMISTRY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "%", 4.0, 5.6, None, 13.0, 120, 3500),
    "LAB-CHM-HBA1C-SUB2": LabTestProfile("LAB-CHM-HBA1C-SUB2", "Glycated Hemoglobin (HbA1c) (Assay Variant #2)", "BIOCHEMISTRY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "%", 4.0, 5.6, None, 13.0, 120, 3500),
    "LAB-CHM-HBA1C-SUB3": LabTestProfile("LAB-CHM-HBA1C-SUB3", "Glycated Hemoglobin (HbA1c) (Assay Variant #3)", "BIOCHEMISTRY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "%", 4.0, 5.6, None, 13.0, 120, 3500),
    "LAB-CHM-HBA1C-SUB4": LabTestProfile("LAB-CHM-HBA1C-SUB4", "Glycated Hemoglobin (HbA1c) (Assay Variant #4)", "BIOCHEMISTRY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "%", 4.0, 5.6, None, 13.0, 120, 3500),
    "LAB-CHM-SOD": LabTestProfile("LAB-CHM-SOD", "Serum Sodium (Na+)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 135.0, 145.0, 120.0, 160.0, 60, 1500),
    "LAB-CHM-SOD-SUB1": LabTestProfile("LAB-CHM-SOD-SUB1", "Serum Sodium (Na+) (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 135.0, 145.0, 120.0, 160.0, 60, 1500),
    "LAB-CHM-SOD-SUB2": LabTestProfile("LAB-CHM-SOD-SUB2", "Serum Sodium (Na+) (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 135.0, 145.0, 120.0, 160.0, 60, 1500),
    "LAB-CHM-SOD-SUB3": LabTestProfile("LAB-CHM-SOD-SUB3", "Serum Sodium (Na+) (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 135.0, 145.0, 120.0, 160.0, 60, 1500),
    "LAB-CHM-SOD-SUB4": LabTestProfile("LAB-CHM-SOD-SUB4", "Serum Sodium (Na+) (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 135.0, 145.0, 120.0, 160.0, 60, 1500),
    "LAB-CHM-POT": LabTestProfile("LAB-CHM-POT", "Serum Potassium (K+)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 3.5, 5.0, 2.8, 6.2, 60, 1500),
    "LAB-CHM-POT-SUB1": LabTestProfile("LAB-CHM-POT-SUB1", "Serum Potassium (K+) (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 3.5, 5.0, 2.8, 6.2, 60, 1500),
    "LAB-CHM-POT-SUB2": LabTestProfile("LAB-CHM-POT-SUB2", "Serum Potassium (K+) (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 3.5, 5.0, 2.8, 6.2, 60, 1500),
    "LAB-CHM-POT-SUB3": LabTestProfile("LAB-CHM-POT-SUB3", "Serum Potassium (K+) (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 3.5, 5.0, 2.8, 6.2, 60, 1500),
    "LAB-CHM-POT-SUB4": LabTestProfile("LAB-CHM-POT-SUB4", "Serum Potassium (K+) (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mEq/L", 3.5, 5.0, 2.8, 6.2, 60, 1500),
    "LAB-CHM-CREAT": LabTestProfile("LAB-CHM-CREAT", "Serum Creatinine", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.7, 1.3, None, 5.0, 60, 1500),
    "LAB-CHM-CREAT-SUB1": LabTestProfile("LAB-CHM-CREAT-SUB1", "Serum Creatinine (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.7, 1.3, None, 5.0, 60, 1500),
    "LAB-CHM-CREAT-SUB2": LabTestProfile("LAB-CHM-CREAT-SUB2", "Serum Creatinine (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.7, 1.3, None, 5.0, 60, 1500),
    "LAB-CHM-CREAT-SUB3": LabTestProfile("LAB-CHM-CREAT-SUB3", "Serum Creatinine (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.7, 1.3, None, 5.0, 60, 1500),
    "LAB-CHM-CREAT-SUB4": LabTestProfile("LAB-CHM-CREAT-SUB4", "Serum Creatinine (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.7, 1.3, None, 5.0, 60, 1500),
    "LAB-CHM-BUN": LabTestProfile("LAB-CHM-BUN", "Blood Urea Nitrogen", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 7.0, 20.0, None, 80.0, 60, 1400),
    "LAB-CHM-BUN-SUB1": LabTestProfile("LAB-CHM-BUN-SUB1", "Blood Urea Nitrogen (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 7.0, 20.0, None, 80.0, 60, 1400),
    "LAB-CHM-BUN-SUB2": LabTestProfile("LAB-CHM-BUN-SUB2", "Blood Urea Nitrogen (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 7.0, 20.0, None, 80.0, 60, 1400),
    "LAB-CHM-BUN-SUB3": LabTestProfile("LAB-CHM-BUN-SUB3", "Blood Urea Nitrogen (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 7.0, 20.0, None, 80.0, 60, 1400),
    "LAB-CHM-BUN-SUB4": LabTestProfile("LAB-CHM-BUN-SUB4", "Blood Urea Nitrogen (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 7.0, 20.0, None, 80.0, 60, 1400),
    "LAB-CHM-BILI-T": LabTestProfile("LAB-CHM-BILI-T", "Total Bilirubin", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.2, 1.2, None, 15.0, 60, 1500),
    "LAB-CHM-BILI-T-SUB1": LabTestProfile("LAB-CHM-BILI-T-SUB1", "Total Bilirubin (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.2, 1.2, None, 15.0, 60, 1500),
    "LAB-CHM-BILI-T-SUB2": LabTestProfile("LAB-CHM-BILI-T-SUB2", "Total Bilirubin (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.2, 1.2, None, 15.0, 60, 1500),
    "LAB-CHM-BILI-T-SUB3": LabTestProfile("LAB-CHM-BILI-T-SUB3", "Total Bilirubin (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.2, 1.2, None, 15.0, 60, 1500),
    "LAB-CHM-BILI-T-SUB4": LabTestProfile("LAB-CHM-BILI-T-SUB4", "Total Bilirubin (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "mg/dL", 0.2, 1.2, None, 15.0, 60, 1500),
    "LAB-CHM-ALT": LabTestProfile("LAB-CHM-ALT", "Alanine Aminotransferase (ALT/SGPT)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 7.0, 56.0, None, 500.0, 60, 1600),
    "LAB-CHM-ALT-SUB1": LabTestProfile("LAB-CHM-ALT-SUB1", "Alanine Aminotransferase (ALT/SGPT) (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 7.0, 56.0, None, 500.0, 60, 1600),
    "LAB-CHM-ALT-SUB2": LabTestProfile("LAB-CHM-ALT-SUB2", "Alanine Aminotransferase (ALT/SGPT) (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 7.0, 56.0, None, 500.0, 60, 1600),
    "LAB-CHM-ALT-SUB3": LabTestProfile("LAB-CHM-ALT-SUB3", "Alanine Aminotransferase (ALT/SGPT) (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 7.0, 56.0, None, 500.0, 60, 1600),
    "LAB-CHM-ALT-SUB4": LabTestProfile("LAB-CHM-ALT-SUB4", "Alanine Aminotransferase (ALT/SGPT) (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 7.0, 56.0, None, 500.0, 60, 1600),
    "LAB-CHM-AST": LabTestProfile("LAB-CHM-AST", "Aspartate Aminotransferase (AST/SGOT)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 10.0, 40.0, None, 500.0, 60, 1600),
    "LAB-CHM-AST-SUB1": LabTestProfile("LAB-CHM-AST-SUB1", "Aspartate Aminotransferase (AST/SGOT) (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 10.0, 40.0, None, 500.0, 60, 1600),
    "LAB-CHM-AST-SUB2": LabTestProfile("LAB-CHM-AST-SUB2", "Aspartate Aminotransferase (AST/SGOT) (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 10.0, 40.0, None, 500.0, 60, 1600),
    "LAB-CHM-AST-SUB3": LabTestProfile("LAB-CHM-AST-SUB3", "Aspartate Aminotransferase (AST/SGOT) (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 10.0, 40.0, None, 500.0, 60, 1600),
    "LAB-CHM-AST-SUB4": LabTestProfile("LAB-CHM-AST-SUB4", "Aspartate Aminotransferase (AST/SGOT) (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "U/L", 10.0, 40.0, None, 500.0, 60, 1600),
    "LAB-CARD-TROP-I": LabTestProfile("LAB-CARD-TROP-I", "High-Sensitivity Troponin I", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/L", 0.0, 14.0, None, 50.0, 30, 4500),
    "LAB-CARD-TROP-I-SUB1": LabTestProfile("LAB-CARD-TROP-I-SUB1", "High-Sensitivity Troponin I (Assay Variant #1)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/L", 0.0, 14.0, None, 50.0, 30, 4500),
    "LAB-CARD-TROP-I-SUB2": LabTestProfile("LAB-CARD-TROP-I-SUB2", "High-Sensitivity Troponin I (Assay Variant #2)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/L", 0.0, 14.0, None, 50.0, 30, 4500),
    "LAB-CARD-TROP-I-SUB3": LabTestProfile("LAB-CARD-TROP-I-SUB3", "High-Sensitivity Troponin I (Assay Variant #3)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/L", 0.0, 14.0, None, 50.0, 30, 4500),
    "LAB-CARD-TROP-I-SUB4": LabTestProfile("LAB-CARD-TROP-I-SUB4", "High-Sensitivity Troponin I (Assay Variant #4)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/L", 0.0, 14.0, None, 50.0, 30, 4500),
    "LAB-CARD-BNP": LabTestProfile("LAB-CARD-BNP", "B-Type Natriuretic Peptide (NT-proBNP)", "IMMUNOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "pg/mL", 0.0, 125.0, None, 1800.0, 45, 5000),
    "LAB-CARD-BNP-SUB1": LabTestProfile("LAB-CARD-BNP-SUB1", "B-Type Natriuretic Peptide (NT-proBNP) (Assay Variant #1)", "IMMUNOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "pg/mL", 0.0, 125.0, None, 1800.0, 45, 5000),
    "LAB-CARD-BNP-SUB2": LabTestProfile("LAB-CARD-BNP-SUB2", "B-Type Natriuretic Peptide (NT-proBNP) (Assay Variant #2)", "IMMUNOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "pg/mL", 0.0, 125.0, None, 1800.0, 45, 5000),
    "LAB-CARD-BNP-SUB3": LabTestProfile("LAB-CARD-BNP-SUB3", "B-Type Natriuretic Peptide (NT-proBNP) (Assay Variant #3)", "IMMUNOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "pg/mL", 0.0, 125.0, None, 1800.0, 45, 5000),
    "LAB-CARD-BNP-SUB4": LabTestProfile("LAB-CARD-BNP-SUB4", "B-Type Natriuretic Peptide (NT-proBNP) (Assay Variant #4)", "IMMUNOLOGY", "WHOLE_BLOOD_EDTA", "LAVENDER_EDTA", "pg/mL", 0.0, 125.0, None, 1800.0, 45, 5000),
    "LAB-INF-CRP": LabTestProfile("LAB-INF-CRP", "C-Reactive Protein (High Sensitivity)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "mg/L", 0.0, 3.0, None, 50.0, 60, 2200),
    "LAB-INF-CRP-SUB1": LabTestProfile("LAB-INF-CRP-SUB1", "C-Reactive Protein (High Sensitivity) (Assay Variant #1)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "mg/L", 0.0, 3.0, None, 50.0, 60, 2200),
    "LAB-INF-CRP-SUB2": LabTestProfile("LAB-INF-CRP-SUB2", "C-Reactive Protein (High Sensitivity) (Assay Variant #2)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "mg/L", 0.0, 3.0, None, 50.0, 60, 2200),
    "LAB-INF-CRP-SUB3": LabTestProfile("LAB-INF-CRP-SUB3", "C-Reactive Protein (High Sensitivity) (Assay Variant #3)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "mg/L", 0.0, 3.0, None, 50.0, 60, 2200),
    "LAB-INF-CRP-SUB4": LabTestProfile("LAB-INF-CRP-SUB4", "C-Reactive Protein (High Sensitivity) (Assay Variant #4)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "mg/L", 0.0, 3.0, None, 50.0, 60, 2200),
    "LAB-INF-PROCALC": LabTestProfile("LAB-INF-PROCALC", "Procalcitonin (Sepsis Biomarker)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/mL", 0.0, 0.05, None, 2.0, 60, 6000),
    "LAB-INF-PROCALC-SUB1": LabTestProfile("LAB-INF-PROCALC-SUB1", "Procalcitonin (Sepsis Biomarker) (Assay Variant #1)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/mL", 0.0, 0.05, None, 2.0, 60, 6000),
    "LAB-INF-PROCALC-SUB2": LabTestProfile("LAB-INF-PROCALC-SUB2", "Procalcitonin (Sepsis Biomarker) (Assay Variant #2)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/mL", 0.0, 0.05, None, 2.0, 60, 6000),
    "LAB-INF-PROCALC-SUB3": LabTestProfile("LAB-INF-PROCALC-SUB3", "Procalcitonin (Sepsis Biomarker) (Assay Variant #3)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/mL", 0.0, 0.05, None, 2.0, 60, 6000),
    "LAB-INF-PROCALC-SUB4": LabTestProfile("LAB-INF-PROCALC-SUB4", "Procalcitonin (Sepsis Biomarker) (Assay Variant #4)", "IMMUNOLOGY", "SERUM", "GOLD_SST", "ng/mL", 0.0, 0.05, None, 2.0, 60, 6000),
    "LAB-CHM-LACTATE": LabTestProfile("LAB-CHM-LACTATE", "Serum L-Lactate (Shock Biomarker)", "BIOCHEMISTRY", "GREEN_HEPARIN", "GREEN_HEPARIN", "mmol/L", 0.5, 2.0, None, 4.0, 20, 3200),
    "LAB-CHM-LACTATE-SUB1": LabTestProfile("LAB-CHM-LACTATE-SUB1", "Serum L-Lactate (Shock Biomarker) (Assay Variant #1)", "BIOCHEMISTRY", "GREEN_HEPARIN", "GREEN_HEPARIN", "mmol/L", 0.5, 2.0, None, 4.0, 20, 3200),
    "LAB-CHM-LACTATE-SUB2": LabTestProfile("LAB-CHM-LACTATE-SUB2", "Serum L-Lactate (Shock Biomarker) (Assay Variant #2)", "BIOCHEMISTRY", "GREEN_HEPARIN", "GREEN_HEPARIN", "mmol/L", 0.5, 2.0, None, 4.0, 20, 3200),
    "LAB-CHM-LACTATE-SUB3": LabTestProfile("LAB-CHM-LACTATE-SUB3", "Serum L-Lactate (Shock Biomarker) (Assay Variant #3)", "BIOCHEMISTRY", "GREEN_HEPARIN", "GREEN_HEPARIN", "mmol/L", 0.5, 2.0, None, 4.0, 20, 3200),
    "LAB-CHM-LACTATE-SUB4": LabTestProfile("LAB-CHM-LACTATE-SUB4", "Serum L-Lactate (Shock Biomarker) (Assay Variant #4)", "BIOCHEMISTRY", "GREEN_HEPARIN", "GREEN_HEPARIN", "mmol/L", 0.5, 2.0, None, 4.0, 20, 3200),
    "LAB-THY-TSH": LabTestProfile("LAB-THY-TSH", "Thyroid Stimulating Hormone", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "uIU/mL", 0.4, 4.0, 0.05, 20.0, 120, 2800),
    "LAB-THY-TSH-SUB1": LabTestProfile("LAB-THY-TSH-SUB1", "Thyroid Stimulating Hormone (Assay Variant #1)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "uIU/mL", 0.4, 4.0, 0.05, 20.0, 120, 2800),
    "LAB-THY-TSH-SUB2": LabTestProfile("LAB-THY-TSH-SUB2", "Thyroid Stimulating Hormone (Assay Variant #2)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "uIU/mL", 0.4, 4.0, 0.05, 20.0, 120, 2800),
    "LAB-THY-TSH-SUB3": LabTestProfile("LAB-THY-TSH-SUB3", "Thyroid Stimulating Hormone (Assay Variant #3)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "uIU/mL", 0.4, 4.0, 0.05, 20.0, 120, 2800),
    "LAB-THY-TSH-SUB4": LabTestProfile("LAB-THY-TSH-SUB4", "Thyroid Stimulating Hormone (Assay Variant #4)", "BIOCHEMISTRY", "SERUM", "GOLD_SST", "uIU/mL", 0.4, 4.0, 0.05, 20.0, 120, 2800),
};

class LabCatalogService:
    @staticmethod
    def get_test(test_code: str) -> Optional[LabTestProfile]:
        return LAB_CATALOG_DATABASE.get(test_code.strip())

    @staticmethod
    def evaluate_result(test_code: str, value: float) -> Dict[str, Any]:
        profile = LabCatalogService.get_test(test_code)
        if not profile:
            return {"status": "UNKNOWN_TEST"}
        is_panic = False
        flag = "NORMAL"
        if profile.critical_panic_low is not None and value <= profile.critical_panic_low:
            is_panic = True
            flag = "CRITICAL_LOW_PANIC"
        elif profile.critical_panic_high is not None and value >= profile.critical_panic_high:
            is_panic = True
            flag = "CRITICAL_HIGH_PANIC"
        elif value < profile.reference_low:
            flag = "LOW"
        elif value > profile.reference_high:
            flag = "HIGH"
        return {
            "flag": flag,
            "is_critical_panic": is_panic,
            "reference_range": f"{profile.reference_low} - {profile.reference_high} {profile.units}",
            "requires_immediate_physician_call": is_panic
        }
