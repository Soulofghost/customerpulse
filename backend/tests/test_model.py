import pytest
from backend.app.engine.churn_model import ChurnModel

def test_churn_low_risk_profile():
    # Long tenure, active usage, zero tickets, annual contract
    res = ChurnModel.predict(
        tenure_months=24,
        monthly_spend=500.0,
        inactivity_days=1,
        support_tickets=0,
        contract_type="Annual",
        feature_usage_score=90.0
    )
    assert res["risk_tier"] == "LOW"
    assert res["churn_probability"] < 0.25
    assert "cross-sell" in res["recommended_action"].lower()

def test_churn_critical_risk_profile():
    # Short tenure, dormant, multiple tickets, month-to-month
    res = ChurnModel.predict(
        tenure_months=2,
        monthly_spend=99.0,
        inactivity_days=30,
        support_tickets=4,
        contract_type="Month-to-Month",
        feature_usage_score=15.0
    )
    assert res["risk_tier"] in ["HIGH", "CRITICAL"]
    assert res["churn_probability"] > 0.60
    assert len(res["feature_contributions"]) >= 5

def test_feature_contributions_ordering():
    res = ChurnModel.predict(12, 199.0, 10, 2, "Month-to-Month", 50.0)
    contribs = res["feature_contributions"]
    assert len(contribs) == 5
    # Largest absolute impact should be first
    assert abs(contribs[0]["impact"]) >= abs(contribs[-1]["impact"])
