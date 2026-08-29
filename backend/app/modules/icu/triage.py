def calculate_sofa_score(pao2_fio2: float, platelets: int, bilirubin: float, map_pressure: float, gcs: int, creatinine: float) -> dict:
    score = 0
    if pao2_fio2 < 200: score += 2
    if platelets < 100: score += 2
    if bilirubin > 2.0: score += 2
    if map_pressure < 70: score += 1
    if gcs < 13: score += 2
    if creatinine > 2.0: score += 2
    
    triage = "CRITICAL_ICU" if score >= 6 else "STEP_DOWN_HIGH_DEPENDENCY" if score >= 3 else "STANDARD_WARD"
    return {"sofa_score": score, "recommended_triage": triage}
