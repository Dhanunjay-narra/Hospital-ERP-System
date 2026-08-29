from app.modules.radiology.dicom_parser import parse_dicom_study_header

def test_dicom_study_parsing():
    res = parse_dicom_study_header("1.2.840.10008.5.1.4.1.1.2", "CT", "PAT-999")
    assert res["is_supported"] is True
    assert res["modality_name"] == "Computed Tomography"
