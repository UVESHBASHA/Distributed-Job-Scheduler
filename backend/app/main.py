from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.organization import router as organization_router
from app.api.v1.project import router as project_router
from app.api.v1.retry_policy import router as retry_policy_router
from app.api.v1.queue import router as queue_router
from app.api.v1.job import router as job_router
from app.api.v1.workers import router as workers_router
from app.api.v1.executions import router as executions_router
from app.api.v1.dead_letter import router as dead_letter_router

app = FastAPI(
    title="Distributed Job Scheduler",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
app.include_router(workers_router)
app.include_router(executions_router)
app.include_router(dead_letter_router)
