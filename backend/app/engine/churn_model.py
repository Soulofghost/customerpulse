import math
from typing import Dict, Any, List

class ChurnModel:
    @staticmethod
    def predict(
        tenure_months: int,
        monthly_spend: float,
        inactivity_days: int,
        support_tickets: int,
        contract_type: str,
        feature_usage_score: float
    ) -> Dict[str, Any]:
        """
        Calibrated logistic classification with individual feature attribution.
        """
        # Baseline bias
        z = -1.2

        contributions = []

        # 1. Inactivity Days effect
        c_inactivity = round(0.075 * inactivity_days, 3)
        z += c_inactivity
        contributions.append({
            "feature": "Inactivity Days",
            "value": f"{inactivity_days} days",
            "impact": c_inactivity,
            "direction": "RISK_INCREASE" if c_inactivity > 0.5 else "NEUTRAL"
        })

        # 2. Support Tickets effect
        c_support = round(0.40 * support_tickets, 3)
        z += c_support
        contributions.append({
            "feature": "Support Tickets / Escalations",
            "value": f"{support_tickets} tickets",
            "impact": c_support,
            "direction": "RISK_INCREASE" if c_support > 0.5 else "NEUTRAL"
        })

        # 3. Contract Type
        is_annual = contract_type.lower() == "annual"
        c_contract = -0.75 if is_annual else 0.45
        z += c_contract
        contributions.append({
            "feature": "Contract Commitment",
            "value": "Annual Contract" if is_annual else "Month-to-Month",
            "impact": c_contract,
            "direction": "RISK_REDUCTION" if is_annual else "RISK_INCREASE"
        })

        # 4. Tenure effect
        c_tenure = round(-0.035 * min(tenure_months, 48), 3)
        z += c_tenure
        contributions.append({
            "feature": "Subscription Tenure",
            "value": f"{tenure_months} months",
            "impact": c_tenure,
            "direction": "RISK_REDUCTION" if abs(c_tenure) > 0.3 else "NEUTRAL"
        })

        # 5. Feature Usage Score (0 - 100)
        c_usage = round(-0.02 * feature_usage_score, 3)
        z += c_usage
        contributions.append({
            "feature": "Product Usage Depth",
            "value": f"{feature_usage_score}/100",
            "impact": c_usage,
            "direction": "RISK_REDUCTION" if feature_usage_score > 60 else "RISK_INCREASE"
        })

        # Sigmoid activation
        p_churn = 1.0 / (1.0 + math.exp(-z))
        p_churn = round(min(0.99, max(0.01, p_churn)), 4)

        # Risk Classification
        if p_churn >= 0.75:
            risk_tier = "CRITICAL"
            top_risk = "Dormant usage and critical open support complaints"
            recommendation = "Deploy Executive Sponsor intervention & offer 20% annual renewal concession."
        elif p_churn >= 0.50:
            risk_tier = "HIGH"
            top_risk = "Rising inactivity or month-to-month contract churn volatility"
            recommendation = "Schedule Customer Success quarterly review & offer onboarding enablement."
        elif p_churn >= 0.25:
            risk_tier = "MEDIUM"
            top_risk = "Feature adoption plateau"
            recommendation = "Send proactive workflow tips & recommend workflow integrations."
        else:
            risk_tier = "LOW"
            top_risk = "Healthy account engagement"
            recommendation = "Identify cross-sell or enterprise tier expansion opportunities."

        return {
            "churn_probability": p_churn,
            "risk_percentage": round(p_churn * 100.0, 1),
            "risk_tier": risk_tier,
            "top_risk_factor": top_risk,
            "recommended_action": recommendation,
            "feature_contributions": sorted(contributions, key=lambda c: abs(c["impact"]), reverse=True)
        }
