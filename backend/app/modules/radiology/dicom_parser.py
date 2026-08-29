from typing import Dict

def parse_dicom_study_header(sop_class_uid: str, modality: str, patient_id: str) -> Dict[str, any]:
    modalities = {"CT": "Computed Tomography", "MR": "Magnetic Resonance", "XR": "X-Ray", "US": "Ultrasound"}
    return {
        "sop_class_uid": sop_class_uid,
        "modality": modality,
        "modality_name": modalities.get(modality.upper(), "Diagnostic Imaging"),
        "patient_id": patient_id,
        "is_supported": modality.upper() in modalities
    }
