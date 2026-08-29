from app.modules.pharmacy.drug_safety import check_drug_interactions

def test_drug_interaction_warnings():
    alerts = check_drug_interactions(["Warfarin", "Aspirin", "Paracetamol"])
    assert len(alerts) == 1
    assert alerts[0]["severity"] == "HIGH"
