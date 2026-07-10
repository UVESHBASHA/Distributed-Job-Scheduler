from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine

app = FastAPI(
    title="Distributed Job Scheduler API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Distributed Job Scheduler API is running!"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "database": "Connected Successfully"
        }
    except Exception as e:
        return {
            "database": "Connection Failed",
            "error": str(e)
        }
