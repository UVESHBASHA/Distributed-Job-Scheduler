from fastapi import FastAPI

app = FastAPI(
    title="Distributed Job Scheduler API",
    description="Production-inspired distributed job scheduling platform",
    version="1.0.0",
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
