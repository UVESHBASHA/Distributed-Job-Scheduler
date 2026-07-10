from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.organization import router as organization_router
from app.api.v1.project import router as project_router
from app.api.v1.retry_policy import router as retry_policy_router
from app.api.v1.queue import router as queue_router
from app.api.v1.job import router as job_router

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
app.include_router(project_router)
app.include_router(retry_policy_router)
app.include_router(queue_router)
app.include_router(job_router)
