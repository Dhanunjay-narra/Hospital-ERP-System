from app.modules.icu.triage import calculate_sofa_score

def test_sofa_triage_calculation():
    res_crit = calculate_sofa_score(pao2_fio2=150, platelets=80, bilirubin=2.5, map_pressure=65, gcs=10, creatinine=2.5)
    assert res_crit["sofa_score"] >= 6
    assert res_crit["recommended_triage"] == "CRITICAL_ICU"
