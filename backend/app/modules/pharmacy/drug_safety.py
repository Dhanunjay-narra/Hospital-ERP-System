from typing import List, Dict

KNOWN_CONTRAINDICATIONS = {
    frozenset(["warfarin", "aspirin"]): "High risk of major hemorrhage and internal bleeding.",
    frozenset(["metformin", "contrast_dye"]): "Risk of lactic acidosis and acute renal failure.",
    frozenset(["lisinopril", "potassium"]): "Severe risk of hyperkalemia and cardiac arrhythmia."
}

def check_drug_interactions(medications: List[str]) -> List[Dict[str, str]]:
    warnings = []
    meds_set = [m.lower().strip() for m in medications]
    for pair, risk in KNOWN_CONTRAINDICATIONS.items():
        if pair.issubset(meds_set):
            warnings.append({"drugs": list(pair), "severity": "HIGH", "warning": risk})
    return warnings
