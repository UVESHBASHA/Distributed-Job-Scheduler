from fastapi import FastAPI

from app.api.v1.auth import router as auth_router

app = FastAPI(
    title="Distributed Job Scheduler",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Distributed Job Scheduler API"
    }

app.include_router(auth_router)
