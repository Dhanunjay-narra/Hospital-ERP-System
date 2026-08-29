from typing import Dict, Any

def convert_patient_to_fhir_r4(patient_id: str, name: str, gender: str, birth_date: str) -> Dict[str, Any]:
    return {
        "resourceType": "Patient",
        "id": patient_id,
        "active": True,
        "name": [{"use": "official", "text": name}],
        "gender": gender.lower(),
        "birthDate": birth_date
    }
