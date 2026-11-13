import os
import sqlite3
from backend.app.config import DB_PATH

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        customer_name TEXT,
        email TEXT,
        company TEXT,
        plan_tier TEXT,
        tenure_months INTEGER,
        monthly_spend REAL,
        inactivity_days INTEGER,
        support_tickets INTEGER,
        contract_type TEXT,
        feature_usage_score REAL,
        churn_probability REAL,
        risk_tier TEXT,
        created_at TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS churn_evaluations (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        churn_probability REAL,
        risk_tier TEXT,
        top_risk_factor TEXT,
        recommended_action TEXT,
        evaluated_at TEXT
    );
    """)

    conn.commit()
    conn.close()

init_db()
