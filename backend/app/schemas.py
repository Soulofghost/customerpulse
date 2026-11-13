from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RegisterCustomerRequest(BaseModel):
    customer_name: str = Field(..., description="Customer or Contact Name")
    email: str = Field(..., description="Business Email Address")
    company: str = Field(..., description="Organization / Account Name")
    plan_tier: Optional[str] = Field(default="Growth")
    tenure_months: int = Field(default=6, ge=1)
    monthly_spend: float = Field(default=299.0, ge=0)
    inactivity_days: int = Field(default=3, ge=0)
    support_tickets: int = Field(default=0, ge=0)
    contract_type: str = Field(default="Annual", description="Annual or Month-to-Month")
    feature_usage_score: float = Field(default=75.0, ge=0, le=100)

class EvaluateChurnRequest(BaseModel):
    customer_name: Optional[str] = Field(default="Custom Prospect")
    email: Optional[str] = Field(default="prospect@company.com")
    company: Optional[str] = Field(default="Prospect Corp")
    plan_tier: Optional[str] = Field(default="Growth")
    tenure_months: int = Field(default=6, ge=1)
    monthly_spend: float = Field(default=299.0, ge=0)
    inactivity_days: int = Field(default=3, ge=0)
    support_tickets: int = Field(default=0, ge=0)
    contract_type: str = Field(default="Annual")
    feature_usage_score: float = Field(default=75.0, ge=0, le=100)

class FeatureImpactItem(BaseModel):
    feature: str
    value: str
    impact: float
    direction: str

class ChurnEvaluationResponse(BaseModel):
    churn_probability: float
    risk_percentage: float
    risk_tier: str
    top_risk_factor: str
    recommended_action: str
    feature_contributions: List[FeatureImpactItem]

class CustomerResponse(BaseModel):
    id: str
    customer_name: str
    email: str
    company: str
    plan_tier: str
    tenure_months: int
    monthly_spend: float
    inactivity_days: int
    support_tickets: int
    contract_type: str
    feature_usage_score: float
    churn_probability: float
    risk_tier: str
    created_at: str
