import math
from typing import Dict, Any, Optional

class ClinicalCalculators:
    @staticmethod
    def calculate_gcs(eye_opening: int, verbal_response: int, motor_response: int) -> Dict[str, Any]:
        """Glasgow Coma Scale: Range 3 - 15"""
        total = max(1, min(4, eye_opening)) + max(1, min(5, verbal_response)) + max(1, min(6, motor_response))
        severity = "MILD_BRAIN_INJURY" if total >= 13 else "MODERATE_BRAIN_INJURY" if total >= 9 else "SEVERE_COMA"
        intubation_indicated = total <= 8
        return {
            "score": total,
            "severity": severity,
            "intubation_indicated": intubation_indicated,
            "interpretation": f"GCS {total}/15: {severity}."
        }

    @staticmethod
    def calculate_sofa(pao2_fio2: float, platelets_k: float, bilirubin_mg_dl: float, map_mmhg: float, gcs_score: int, creatinine_mg_dl: float) -> Dict[str, Any]:
        """Sequential Organ Failure Assessment (SOFA) Score (0 - 24)"""
        score = 0
        if pao2_fio2 < 100: score += 4
        elif pao2_fio2 < 200: score += 3
        elif pao2_fio2 < 300: score += 2
        elif pao2_fio2 < 400: score += 1

        if platelets_k < 20: score += 4
        elif platelets_k < 50: score += 3
        elif platelets_k < 100: score += 2
        elif platelets_k < 150: score += 1

        if bilirubin_mg_dl >= 12.0: score += 4
        elif bilirubin_mg_dl >= 6.0: score += 3
        elif bilirubin_mg_dl >= 2.0: score += 2
        elif bilirubin_mg_dl >= 1.2: score += 1

        if map_mmhg < 70: score += 1

        if gcs_score < 6: score += 4
        elif gcs_score <= 9: score += 3
        elif gcs_score <= 12: score += 2
        elif gcs_score <= 14: score += 1

        if creatinine_mg_dl >= 5.0: score += 4
        elif creatinine_mg_dl >= 3.5: score += 3
        elif creatinine_mg_dl >= 2.0: score += 2
        elif creatinine_mg_dl >= 1.2: score += 1

        return {
            "sofa_score": score,
            "is_septic_shock_probable": score >= 2
        }

    @staticmethod
    def calculate_gfr_cockcroft_gault(age_years: int, weight_kg: float, serum_creatinine: float, is_female: bool) -> float:
        """Calculates Creatinine Clearance (eGFR) in mL/min"""
        if serum_creatinine <= 0:
            return 120.0
        cr_cl = ((140 - age_years) * weight_kg) / (72 * serum_creatinine)
        if is_female:
            cr_cl *= 0.85
        return round(cr_cl, 2)

    @staticmethod
    def calculate_curb65(confusion: bool, bun_mg_dl: float, resp_rate: int, sbp: int, dbp: int, age_years: int) -> Dict[str, Any]:
        """Pneumonia Mortality Risk CURB-65 Score (0 - 5)"""
        score = 0
        if confusion: score += 1
        if bun_mg_dl > 19: score += 1
        if resp_rate >= 30: score += 1
        if sbp < 90 or dbp <= 60: score += 1
        if age_years >= 65: score += 1
        return {"curb65_score": score}

    @staticmethod
    def calculate_cha2ds2_vasc(age: int, is_female: bool, chf: bool, hypertension: bool, stroke_tia_history: bool, vascular_disease: bool, diabetes: bool) -> Dict[str, Any]:
        """Atrial Fibrillation Stroke Risk CHA2DS2-VASc Score (0 - 9)"""
        score = 0
        if chf: score += 1
        if hypertension: score += 1
        if age >= 75: score += 2
        elif age >= 65: score += 1
        if diabetes: score += 1
        if stroke_tia_history: score += 2
        if vascular_disease: score += 1
        if is_female: score += 1
        return {
            "score": score,
            "oral_anticoagulation_recommended": (score >= 2 if not is_female else score >= 3)
        }
