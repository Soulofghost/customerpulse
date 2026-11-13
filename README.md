# CustomerPulse - Customer Churn Prediction & Retention Analytics

CustomerPulse is a predictive machine learning platform that evaluates customer churn risk and prescribes targeted retention playbooks for SaaS and subscription businesses. Built with Python 3.11, FastAPI, and SQLite WAL, CustomerPulse utilizes calibrated logistic regression classification and feature impact attribution to proactively prevent revenue churn.

## Core Capabilities
- **Explainable Churn Risk Model:** Evaluates account health based on subscription tenure, monthly spend, inactivity recency, support ticket escalation rate, contract commitment, and feature usage depth.
- **Log-Odds Impact Attribution:** Decomposes the individual contribution of each behavioral metric to explain exact risk drivers.
- **Risk Categorization:** Automatically segments customer portfolios into Low, Medium, High, and Critical risk tiers.
- **Automated Retention Playbooks:** Prescribes actionable intervention workflows (Executive sponsor deployment, CSM health checks, annual contract renewal incentives).
- **Interactive What-If Simulation:** Real-time parameter tweaking to model intervention impact on retention probability.

## Technology Stack
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, Pytest
- **Database:** SQLite (WAL mode)
- **Frontend:** Vanilla JavaScript, Modern CSS Flex/Grid, Dark Customer Success UI
- **DevOps:** Docker, Docker Compose, GitHub Actions CI

## Quickstart

```bash
# Clone the repository
git clone https://github.com/Soulofghost/customerpulse.git
cd customerpulse

# Install dependencies
pip install -r backend/requirements.txt

# Run test suite
pytest -v

# Run the local API server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints
- `GET /api/health` - Service health and classifier engine status.
- `GET /api/stats` - Portfolio metrics (total accounts, at-risk count, average risk %, MRR at risk).
- `GET /api/customers` - List scored accounts ordered by churn probability.
- `POST /api/customers` - Register and score a new customer account.
- `POST /api/predict` - Real-time what-if simulation on arbitrary customer parameters.

## Author
Alvin MS ([@Soulofghost](https://github.com/Soulofghost))
