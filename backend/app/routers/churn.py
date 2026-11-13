import uuid
import datetime
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from backend.app.database import get_connection
from backend.app.schemas import (
    RegisterCustomerRequest, CustomerResponse,
    EvaluateChurnRequest, ChurnEvaluationResponse
)
from backend.app.engine.churn_model import ChurnModel

router = APIRouter(prefix="/api", tags=["churn"])

@router.get("/health")
def healthcheck():
    return {
        "status": "ok",
        "service": "CustomerPulse",
        "version": "1.0.0",
        "engine": "Calibrated Logistic Regression & Explainable Churn Risk Classifier"
    }

@router.get("/stats")
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as c FROM customers;")
    total_customers = cursor.fetchone()["c"]

    cursor.execute("SELECT COUNT(*) as c FROM customers WHERE risk_tier IN ('HIGH', 'CRITICAL');")
    at_risk_count = cursor.fetchone()["c"]

    cursor.execute("SELECT AVG(churn_probability) as a FROM customers;")
    avg_churn_row = cursor.fetchone()["a"]
    avg_churn = round(avg_churn_row * 100.0, 1) if avg_churn_row else 0.0

    cursor.execute("SELECT SUM(monthly_spend) as s FROM customers WHERE risk_tier IN ('HIGH', 'CRITICAL');")
    revenue_at_risk_row = cursor.fetchone()["s"]
    revenue_at_risk = round(revenue_at_risk_row, 2) if revenue_at_risk_row else 0.0

    conn.close()

    return {
        "totalCustomers": total_customers,
        "atRiskAccounts": at_risk_count,
        "averageChurnRisk": avg_churn,
        "monthlyRevenueAtRisk": revenue_at_risk
    }

@router.get("/customers", response_model=List[CustomerResponse])
def list_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY churn_probability DESC;")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def register_customer(payload: RegisterCustomerRequest):
    pred = ChurnModel.predict(
        payload.tenure_months,
        payload.monthly_spend,
        payload.inactivity_days,
        payload.support_tickets,
        payload.contract_type,
        payload.feature_usage_score
    )

    cust_id = "cust-" + str(uuid.uuid4())[:8]
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO customers (id, customer_name, email, company, plan_tier, tenure_months, monthly_spend, inactivity_days, support_tickets, contract_type, feature_usage_score, churn_probability, risk_tier, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        cust_id,
        payload.customer_name,
        payload.email,
        payload.company,
        payload.plan_tier or "Growth",
        payload.tenure_months,
        payload.monthly_spend,
        payload.inactivity_days,
        payload.support_tickets,
        payload.contract_type,
        payload.feature_usage_score,
        pred["churn_probability"],
        pred["risk_tier"],
        now_iso
    ))

    cursor.execute("""
    INSERT INTO churn_evaluations (id, customer_id, churn_probability, risk_tier, top_risk_factor, recommended_action, evaluated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (str(uuid.uuid4()), cust_id, pred["churn_probability"], pred["risk_tier"], pred["top_risk_factor"], pred["recommended_action"], now_iso))

    conn.commit()
    conn.close()

    return {
        "id": cust_id,
        "customer_name": payload.customer_name,
        "email": payload.email,
        "company": payload.company,
        "plan_tier": payload.plan_tier or "Growth",
        "tenure_months": payload.tenure_months,
        "monthly_spend": payload.monthly_spend,
        "inactivity_days": payload.inactivity_days,
        "support_tickets": payload.support_tickets,
        "contract_type": payload.contract_type,
        "feature_usage_score": payload.feature_usage_score,
        "churn_probability": pred["churn_probability"],
        "risk_tier": pred["risk_tier"],
        "created_at": now_iso
    }

@router.post("/predict", response_model=ChurnEvaluationResponse)
def evaluate_custom_profile(payload: RegisterCustomerRequest):
    return ChurnModel.predict(
        payload.tenure_months,
        payload.monthly_spend,
        payload.inactivity_days,
        payload.support_tickets,
        payload.contract_type,
        payload.feature_usage_score
    )
