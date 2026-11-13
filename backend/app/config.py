import os

PORT = int(os.getenv("CUSTOMERPULSE_PORT", "8000"))
DB_PATH = os.getenv("CUSTOMERPULSE_DB_PATH", "backend/data/customerpulse.db")
