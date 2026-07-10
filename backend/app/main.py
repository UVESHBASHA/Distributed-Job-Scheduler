from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.organization import router as organization_router

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
app.include_router(organization_router)
