"""
HL7 v2.5.1 Electronic Healthcare Data Interchange Engine
Encodes and decodes MSH, PID, PV1, OBR, OBX, and DG1 clinical messages for hospital interoperability.
"""
import datetime
from typing import Dict, List, Any, Optional

class HL7MessageEngine:
    FIELD_SEPARATOR = "|"
    COMPONENT_SEPARATOR = "^"

    @staticmethod
    def build_adt_a01(patient_uhid: str, patient_name: str, dob_yyyymmdd: str, gender: str, room_bed: str, admitting_doctor: str) -> str:
        """Builds HL7 ADT^A01 Inpatient Admission Notification Message"""
        ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        msg_ctrl_id = f"MSG-{ts}"
        segments = [
            f"MSH|^~\\&|APEX_HIS|APEX_MAIN|EXT_LIS|CENTRAL|{ts}||ADT^A01|{msg_ctrl_id}|P|2.5.1",
            f"EVN|A01|{ts}",
            f"PID|1||{patient_uhid}^^^APEX_HOSPITAL^MR||{patient_name}||{dob_yyyymmdd}|{gender}",
            f"PV1|1|I|{room_bed}||||{admitting_doctor}^^^DR|||||||||||{ts}",
        ]
        return "\r".join(segments)

    @staticmethod
    def build_oru_r01(patient_uhid: str, order_num: str, test_code: str, test_name: str, result_value: str, units: str, ref_range: str, abnormal_flag: str) -> str:
        """Builds HL7 ORU^R01 Observational Diagnostic Lab Result Message"""
        ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        msg_ctrl_id = f"LAB-{ts}"
        segments = [
            f"MSH|^~\\&|APEX_LIS|LAB_DEPT|APEX_EMR|CLINICAL|{ts}||ORU^R01|{msg_ctrl_id}|P|2.5.1",
            f"PID|1||{patient_uhid}^^^APEX_HOSPITAL^MR",
            f"OBR|1|{order_num}|{order_num}|{test_code}^{test_name}^LN|||{ts}",
            f"OBX|1|NM|{test_code}^{test_name}^LN||{result_value}|{units}|{ref_range}|{abnormal_flag}|||F|||{ts}",
        ]
        return "\r".join(segments)

    @staticmethod
    def parse_message(hl7_raw: str) -> Dict[str, Any]:
        lines = [line.strip() for line in hl7_raw.split("\r") if line.strip()]
        parsed_segments = {}
        for line in lines:
            parts = line.split("|")
            seg_name = parts[0]
            parsed_segments[seg_name] = parts[1:]
        return parsed_segments
