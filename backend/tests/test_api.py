import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_healthcheck():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["service"] == "CustomerPulse"

def test_stats_endpoint():
    res = client.get("/api/stats")
    assert res.status_code == 200
    data = res.json()
    assert "totalCustomers" in data
    assert "atRiskAccounts" in data

def test_register_customer_and_list():
    payload = {
        "customer_name": "Sarah Connor",
        "email": "sarah@cyberdyne.io",
        "company": "Cyberdyne Systems",
        "plan_tier": "Enterprise",
        "tenure_months": 18,
        "monthly_spend": 1200.0,
        "inactivity_days": 2,
        "support_tickets": 1,
        "contract_type": "Annual",
        "feature_usage_score": 85.0
    }
    res = client.post("/api/customers", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["customer_name"] == "Sarah Connor"
    assert data["risk_tier"] in ["LOW", "MEDIUM"]

    list_res = client.get("/api/customers")
    assert list_res.status_code == 200
    assert any(c["email"] == "sarah@cyberdyne.io" for c in list_res.json())

def test_predict_endpoint():
    payload = {
        "customer_name": "Test User",
        "email": "test@domain.com",
        "company": "Test Co",
        "tenure_months": 3,
        "monthly_spend": 50.0,
        "inactivity_days": 25,
        "support_tickets": 3,
        "contract_type": "Month-to-Month",
        "feature_usage_score": 20.0
    }
    res = client.post("/api/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["churn_probability"] > 0.50
    assert "feature_contributions" in data
