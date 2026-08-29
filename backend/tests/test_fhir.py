from app.core.fhir_engine import convert_patient_to_fhir_r4

def test_fhir_r4_patient_serialization():
    res = convert_patient_to_fhir_r4("PAT-101", "John Doe", "male", "1985-06-15")
    assert res["resourceType"] == "Patient"
    assert res["id"] == "PAT-101"
    assert res["gender"] == "male"
