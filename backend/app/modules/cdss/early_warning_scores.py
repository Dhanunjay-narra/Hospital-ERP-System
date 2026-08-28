"""
National Early Warning Score 2 (NEWS2) & Deterioration Early Detection Protocol
Royal College of Physicians validated acute illness clinical scoring algorithm.
"""
from typing import Dict, Any

class EarlyWarningScoringEngine:
    @staticmethod
    def calculate_news2(resp_rate: int, spo2_scale1: float, on_supplemental_oxygen: bool, systolic_bp: int, pulse_rate: int, consciousness_alert: bool, temperature_c: float) -> Dict[str, Any]:
        score = 0
        # Respiration rate
        if resp_rate <= 8:
            score += 3
        elif resp_rate in [9, 10, 11]:
            score += 1
        elif resp_rate in range(12, 21):
            score += 0
        elif resp_rate in [21, 22, 23, 24]:
            score += 2
        else:
            score += 3
        # SpO2 Scale 1
        if spo2_scale1 <= 91:
            score += 3
        elif spo2_scale1 in [92, 93]:
            score += 2
        elif spo2_scale1 in [94, 95]:
            score += 1
        else:
            score += 0
        # Oxygen requirement
        if on_supplemental_oxygen:
            score += 2
        # Systolic Blood Pressure
        if systolic_bp <= 90:
            score += 3
        elif systolic_bp in range(91, 101):
            score += 2
        elif systolic_bp in range(101, 111):
            score += 1
        elif systolic_bp in range(111, 220):
            score += 0
        else:
            score += 3
        # Pulse rate
        if pulse_rate <= 40:
            score += 3
        elif pulse_rate in range(41, 51):
            score += 1
        elif pulse_rate in range(51, 91):
            score += 0
        elif pulse_rate in range(91, 111):
            score += 1
        elif pulse_rate in range(111, 131):
            score += 2
        else:
            score += 3
        # Consciousness (ACVPU)
        if not consciousness_alert:
            score += 3
        # Temperature
        if temperature_c <= 35.0:
            score += 3
        elif 35.1 <= temperature_c <= 36.0:
            score += 1
        elif 36.1 <= temperature_c <= 38.0:
            score += 0
        elif 38.1 <= temperature_c <= 39.0:
            score += 1
        else:
            score += 2
        risk_level = "LOW_RISK" if score <= 4 else "MEDIUM_RISK" if score in [5, 6] else "HIGH_CRITICAL_DETERIORATION"
        monitoring = "Minimum 12-hourly" if score == 0 else "Minimum 4-6 hourly" if score <= 4 else "Minimum 1-hourly monitoring & Urgent Medical Assessment" if score <= 6 else "Continuous vital monitoring & Immediate Emergency Medical Team (MET/RRT) Escalation"
        return {
            "news2_total_score": score,
            "clinical_risk_tier": risk_level,
            "mandatory_monitoring_frequency": monitoring,
            "trigger_rapid_response_team": score >= 7
        }
