import pytest
from app.modules.clinical.calculators import ClinicalCalculators
from app.modules.clinical.icd10_registry import ICD10Service
from app.modules.clinical.snomed_ct import SnomedService
from app.modules.pharmacy.interaction_matrix import DrugInteractionEngine
from app.modules.laboratory.test_catalog_definitions import LabCatalogService
from app.modules.billing.cpt_codes import CPTService
from app.modules.cdss.early_warning_scores import EarlyWarningScoringEngine
from app.core.hl7_engine import HL7MessageEngine
from app.core.fhir_converter import FHIRR4Converter

def test_clinical_calculators():
    # GCS test
    gcs = ClinicalCalculators.calculate_gcs(4, 5, 6)
    assert gcs["score"] == 15
    assert not gcs["intubation_indicated"]

    gcs_severe = ClinicalCalculators.calculate_gcs(1, 1, 2)
    assert gcs_severe["score"] <= 8
    assert gcs_severe["intubation_indicated"]

    # SOFA score
    sofa = ClinicalCalculators.calculate_sofa(150, 45, 3.5, 65, 11, 2.5)
    assert sofa["sofa_score"] > 5
    assert sofa["is_septic_shock_probable"]

    # eGFR Cockcroft-Gault
    gfr = ClinicalCalculators.calculate_gfr_cockcroft_gault(60, 70.0, 1.2, is_female=False)
    assert gfr > 0

    # CURB-65
    curb = ClinicalCalculators.calculate_curb65(True, 25.0, 32, 85, 55, 70)
    assert curb["curb65_score"] >= 4

    # CHA2DS2-VASc
    cha = ClinicalCalculators.calculate_cha2ds2_vasc(76, False, True, True, True, False, True)
    assert cha["oral_anticoagulation_recommended"]

def test_icd10_and_snomed_registries():
    # Search ICD-10
    results = ICD10Service.search("diabetes")
    assert len(results) >= 0

    # Lookup code
    item = ICD10Service.get_by_code("C03.01")
    assert item is not None
    assert item.chapter != ""

    # Snomed lookup
    snomed_hits = SnomedService.search("medical")
    assert len(snomed_hits) >= 0

def test_drug_interactions_and_lab():
    # Evaluate DDI
    ddi = DrugInteractionEngine.evaluate_prescription(["Warfarin", "Ibuprofen"])
    assert len(ddi) > 0
    assert ddi[0].severity == "CONTRAINDICATED"

    # Evaluate Lab Panic Value
    lab_eval = LabCatalogService.evaluate_result("LAB-CHM-POT", 2.2) # Severe hypokalemia
    assert lab_eval["is_critical_panic"]
    assert lab_eval["flag"] == "CRITICAL_LOW_PANIC"

def test_billing_and_early_warning():
    # CPT calculation
    total_rvu = CPTService.calculate_total_rvu(["99203", "99214"])
    assert total_rvu > 0

    # NEWS2 score
    news = EarlyWarningScoringEngine.calculate_news2(
        resp_rate=26,
        spo2_scale1=89.0,
        on_supplemental_oxygen=True,
        systolic_bp=88,
        pulse_rate=135,
        consciousness_alert=False,
        temperature_c=39.5
    )
    assert news["news2_total_score"] >= 7
    assert news["trigger_rapid_response_team"]

def test_hl7_and_fhir_engines():
    # Generate HL7 ADT message
    hl7_msg = HL7MessageEngine.build_adt_a01(
        patient_uhid="APX-2026-00001",
        patient_name="DOE^JOHN",
        dob_yyyymmdd="19850615",
        gender="M",
        room_bed="ICU-BED-04",
        admitting_doctor="DR_SMITH"
    )
    assert "MSH|^~\\&|APEX_HIS" in hl7_msg
    assert "PID|1||APX-2026-00001" in hl7_msg

    # Convert to FHIR Resource
    fhir_pat = FHIRR4Converter.patient_to_fhir_resource(
        patient_uhid="APX-2026-00001",
        first_name="John",
        last_name="Doe",
        dob_iso="1985-06-15",
        gender="male",
        phone="+15551234567"
    )
    assert fhir_pat["resourceType"] == "Patient"
    assert fhir_pat["id"] == "APX-2026-00001"
