"""
ApexCare Fast Healthcare Interoperability Resources (FHIR R4) Schema Transformer
Transforms native models to HL7 FHIR JSON-LD resources.
"""
import datetime
from typing import Dict, List, Any, Optional

class FHIRR4Converter:
    @staticmethod
    def patient_to_fhir_resource(patient_uhid: str, first_name: str, last_name: str, dob_iso: str, gender: str, phone: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
        return {
            "resourceType": "Patient",
            "id": patient_uhid,
            "identifier": [
                {
                    "use": "usual",
                    "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR"}]},
                    "system": "urn:oid:apexcare.hospital.uhid",
                    "value": patient_uhid,
                }
            ],
            "name": [{"use": "official", "family": last_name, "given": [first_name]}],
            "gender": gender.lower() if gender else "unknown",
            "birthDate": dob_iso[:10] if dob_iso else None,
            "telecom": [
                {"system": "phone", "value": phone, "use": "mobile"} if phone else {},
                {"system": "email", "value": email, "use": "home"} if email else {},
            ],
        }

    @staticmethod
    def observation_to_fhir(obs_id: str, patient_uhid: str, loinc_code: str, test_name: str, value: float, unit: str, ref_low: float, ref_high: float) -> Dict[str, Any]:
        return {
            "resourceType": "Observation",
            "id": obs_id,
            "status": "final",
            "code": {
                "coding": [{"system": "http://loinc.org", "code": loinc_code, "display": test_name}],
                "text": test_name,
            },
            "subject": {"reference": f"Patient/{patient_uhid}"},
            "valueQuantity": {"value": value, "unit": unit, "system": "http://unitsofmeasure.org"},
            "referenceRange": [{"low": {"value": ref_low, "unit": unit}, "high": {"value": ref_high, "unit": unit}}],
        }
    @staticmethod
    def transform_specialized_resource_1(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #1"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/1", "valueString": f"Specialty Extension Metadata #1"}],
        }

    @staticmethod
    def transform_specialized_resource_2(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #2"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/2", "valueString": f"Specialty Extension Metadata #2"}],
        }

    @staticmethod
    def transform_specialized_resource_3(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #3"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/3", "valueString": f"Specialty Extension Metadata #3"}],
        }

    @staticmethod
    def transform_specialized_resource_4(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #4"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/4", "valueString": f"Specialty Extension Metadata #4"}],
        }

    @staticmethod
    def transform_specialized_resource_5(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #5"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/5", "valueString": f"Specialty Extension Metadata #5"}],
        }

    @staticmethod
    def transform_specialized_resource_6(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #6"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/6", "valueString": f"Specialty Extension Metadata #6"}],
        }

    @staticmethod
    def transform_specialized_resource_7(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #7"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/7", "valueString": f"Specialty Extension Metadata #7"}],
        }

    @staticmethod
    def transform_specialized_resource_8(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #8"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/8", "valueString": f"Specialty Extension Metadata #8"}],
        }

    @staticmethod
    def transform_specialized_resource_9(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #9"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/9", "valueString": f"Specialty Extension Metadata #9"}],
        }

    @staticmethod
    def transform_specialized_resource_10(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #10"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/10", "valueString": f"Specialty Extension Metadata #10"}],
        }

    @staticmethod
    def transform_specialized_resource_11(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #11"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/11", "valueString": f"Specialty Extension Metadata #11"}],
        }

    @staticmethod
    def transform_specialized_resource_12(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #12"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/12", "valueString": f"Specialty Extension Metadata #12"}],
        }

    @staticmethod
    def transform_specialized_resource_13(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #13"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/13", "valueString": f"Specialty Extension Metadata #13"}],
        }

    @staticmethod
    def transform_specialized_resource_14(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #14"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/14", "valueString": f"Specialty Extension Metadata #14"}],
        }

    @staticmethod
    def transform_specialized_resource_15(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #15"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/15", "valueString": f"Specialty Extension Metadata #15"}],
        }

    @staticmethod
    def transform_specialized_resource_16(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #16"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/16", "valueString": f"Specialty Extension Metadata #16"}],
        }

    @staticmethod
    def transform_specialized_resource_17(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #17"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/17", "valueString": f"Specialty Extension Metadata #17"}],
        }

    @staticmethod
    def transform_specialized_resource_18(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #18"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/18", "valueString": f"Specialty Extension Metadata #18"}],
        }

    @staticmethod
    def transform_specialized_resource_19(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #19"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/19", "valueString": f"Specialty Extension Metadata #19"}],
        }

    @staticmethod
    def transform_specialized_resource_20(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #20"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/20", "valueString": f"Specialty Extension Metadata #20"}],
        }

    @staticmethod
    def transform_specialized_resource_21(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #21"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/21", "valueString": f"Specialty Extension Metadata #21"}],
        }

    @staticmethod
    def transform_specialized_resource_22(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #22"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/22", "valueString": f"Specialty Extension Metadata #22"}],
        }

    @staticmethod
    def transform_specialized_resource_23(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #23"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/23", "valueString": f"Specialty Extension Metadata #23"}],
        }

    @staticmethod
    def transform_specialized_resource_24(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #24"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/24", "valueString": f"Specialty Extension Metadata #24"}],
        }

    @staticmethod
    def transform_specialized_resource_25(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #25"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/25", "valueString": f"Specialty Extension Metadata #25"}],
        }

    @staticmethod
    def transform_specialized_resource_26(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #26"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/26", "valueString": f"Specialty Extension Metadata #26"}],
        }

    @staticmethod
    def transform_specialized_resource_27(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #27"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/27", "valueString": f"Specialty Extension Metadata #27"}],
        }

    @staticmethod
    def transform_specialized_resource_28(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #28"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/28", "valueString": f"Specialty Extension Metadata #28"}],
        }

    @staticmethod
    def transform_specialized_resource_29(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #29"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/29", "valueString": f"Specialty Extension Metadata #29"}],
        }

    @staticmethod
    def transform_specialized_resource_30(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #30"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/30", "valueString": f"Specialty Extension Metadata #30"}],
        }

    @staticmethod
    def transform_specialized_resource_31(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #31"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/31", "valueString": f"Specialty Extension Metadata #31"}],
        }

    @staticmethod
    def transform_specialized_resource_32(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #32"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/32", "valueString": f"Specialty Extension Metadata #32"}],
        }

    @staticmethod
    def transform_specialized_resource_33(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #33"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/33", "valueString": f"Specialty Extension Metadata #33"}],
        }

    @staticmethod
    def transform_specialized_resource_34(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #34"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/34", "valueString": f"Specialty Extension Metadata #34"}],
        }

    @staticmethod
    def transform_specialized_resource_35(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #35"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/35", "valueString": f"Specialty Extension Metadata #35"}],
        }

    @staticmethod
    def transform_specialized_resource_36(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #36"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/36", "valueString": f"Specialty Extension Metadata #36"}],
        }

    @staticmethod
    def transform_specialized_resource_37(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #37"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/37", "valueString": f"Specialty Extension Metadata #37"}],
        }

    @staticmethod
    def transform_specialized_resource_38(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #38"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/38", "valueString": f"Specialty Extension Metadata #38"}],
        }

    @staticmethod
    def transform_specialized_resource_39(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #39"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/39", "valueString": f"Specialty Extension Metadata #39"}],
        }

    @staticmethod
    def transform_specialized_resource_40(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #40"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/40", "valueString": f"Specialty Extension Metadata #40"}],
        }

    @staticmethod
    def transform_specialized_resource_41(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #41"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/41", "valueString": f"Specialty Extension Metadata #41"}],
        }

    @staticmethod
    def transform_specialized_resource_42(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #42"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/42", "valueString": f"Specialty Extension Metadata #42"}],
        }

    @staticmethod
    def transform_specialized_resource_43(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #43"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/43", "valueString": f"Specialty Extension Metadata #43"}],
        }

    @staticmethod
    def transform_specialized_resource_44(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #44"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/44", "valueString": f"Specialty Extension Metadata #44"}],
        }

    @staticmethod
    def transform_specialized_resource_45(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #45"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/45", "valueString": f"Specialty Extension Metadata #45"}],
        }

    @staticmethod
    def transform_specialized_resource_46(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #46"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/46", "valueString": f"Specialty Extension Metadata #46"}],
        }

    @staticmethod
    def transform_specialized_resource_47(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #47"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/47", "valueString": f"Specialty Extension Metadata #47"}],
        }

    @staticmethod
    def transform_specialized_resource_48(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #48"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/48", "valueString": f"Specialty Extension Metadata #48"}],
        }

    @staticmethod
    def transform_specialized_resource_49(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #49"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/49", "valueString": f"Specialty Extension Metadata #49"}],
        }

    @staticmethod
    def transform_specialized_resource_50(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #50"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/50", "valueString": f"Specialty Extension Metadata #50"}],
        }

    @staticmethod
    def transform_specialized_resource_51(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #51"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/51", "valueString": f"Specialty Extension Metadata #51"}],
        }

    @staticmethod
    def transform_specialized_resource_52(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #52"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/52", "valueString": f"Specialty Extension Metadata #52"}],
        }

    @staticmethod
    def transform_specialized_resource_53(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #53"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/53", "valueString": f"Specialty Extension Metadata #53"}],
        }

    @staticmethod
    def transform_specialized_resource_54(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #54"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/54", "valueString": f"Specialty Extension Metadata #54"}],
        }

    @staticmethod
    def transform_specialized_resource_55(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #55"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/55", "valueString": f"Specialty Extension Metadata #55"}],
        }

    @staticmethod
    def transform_specialized_resource_56(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #56"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/56", "valueString": f"Specialty Extension Metadata #56"}],
        }

    @staticmethod
    def transform_specialized_resource_57(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #57"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/57", "valueString": f"Specialty Extension Metadata #57"}],
        }

    @staticmethod
    def transform_specialized_resource_58(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #58"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/58", "valueString": f"Specialty Extension Metadata #58"}],
        }

    @staticmethod
    def transform_specialized_resource_59(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #59"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/59", "valueString": f"Specialty Extension Metadata #59"}],
        }

    @staticmethod
    def transform_specialized_resource_60(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #60"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/60", "valueString": f"Specialty Extension Metadata #60"}],
        }

    @staticmethod
    def transform_specialized_resource_61(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #61"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/61", "valueString": f"Specialty Extension Metadata #61"}],
        }

    @staticmethod
    def transform_specialized_resource_62(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #62"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/62", "valueString": f"Specialty Extension Metadata #62"}],
        }

    @staticmethod
    def transform_specialized_resource_63(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #63"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/63", "valueString": f"Specialty Extension Metadata #63"}],
        }

    @staticmethod
    def transform_specialized_resource_64(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #64"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/64", "valueString": f"Specialty Extension Metadata #64"}],
        }

    @staticmethod
    def transform_specialized_resource_65(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #65"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/65", "valueString": f"Specialty Extension Metadata #65"}],
        }

    @staticmethod
    def transform_specialized_resource_66(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #66"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/66", "valueString": f"Specialty Extension Metadata #66"}],
        }

    @staticmethod
    def transform_specialized_resource_67(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #67"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/67", "valueString": f"Specialty Extension Metadata #67"}],
        }

    @staticmethod
    def transform_specialized_resource_68(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #68"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/68", "valueString": f"Specialty Extension Metadata #68"}],
        }

    @staticmethod
    def transform_specialized_resource_69(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #69"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/69", "valueString": f"Specialty Extension Metadata #69"}],
        }

    @staticmethod
    def transform_specialized_resource_70(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #70"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/70", "valueString": f"Specialty Extension Metadata #70"}],
        }

    @staticmethod
    def transform_specialized_resource_71(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #71"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/71", "valueString": f"Specialty Extension Metadata #71"}],
        }

    @staticmethod
    def transform_specialized_resource_72(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #72"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/72", "valueString": f"Specialty Extension Metadata #72"}],
        }

    @staticmethod
    def transform_specialized_resource_73(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #73"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/73", "valueString": f"Specialty Extension Metadata #73"}],
        }

    @staticmethod
    def transform_specialized_resource_74(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #74"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/74", "valueString": f"Specialty Extension Metadata #74"}],
        }

    @staticmethod
    def transform_specialized_resource_75(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #75"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/75", "valueString": f"Specialty Extension Metadata #75"}],
        }

    @staticmethod
    def transform_specialized_resource_76(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #76"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/76", "valueString": f"Specialty Extension Metadata #76"}],
        }

    @staticmethod
    def transform_specialized_resource_77(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #77"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/77", "valueString": f"Specialty Extension Metadata #77"}],
        }

    @staticmethod
    def transform_specialized_resource_78(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #78"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/78", "valueString": f"Specialty Extension Metadata #78"}],
        }

    @staticmethod
    def transform_specialized_resource_79(resource_id: str, patient_ref: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resourceType": "Encounter",
            "id": resource_id,
            "status": "finished",
            "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"},
            "subject": {"reference": f"Patient/{patient_ref}"},
            "serviceProvider": {"display": "ApexCare Hospital Specialty Department #79"},
            "period": {"start": datetime.datetime.utcnow().isoformat(), "end": datetime.datetime.utcnow().isoformat()},
            "extension": [{"url": "http://apexcare.health/fhir/extension/79", "valueString": f"Specialty Extension Metadata #79"}],
        }
