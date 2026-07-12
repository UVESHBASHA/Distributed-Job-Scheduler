# Distributed Job Scheduler

A production-inspired distributed job scheduling platform designed to reliably execute asynchronous background jobs across multiple workers.

The system demonstrates distributed job processing, concurrency control, priority scheduling, retries, worker health monitoring, crash recovery, and dead-letter queue handling.

## Features

### Job Management
- Create immediate jobs
- Schedule jobs using `run_at`
- Recurring jobs using cron expressions
- Batch job creation
- Priority-based job execution
- Job cancellation
- Idempotency keys for duplicate job prevention
- Job lifecycle and state validation

### Distributed Workers
- Multiple worker support
- Concurrent job execution
- Atomic job claiming using PostgreSQL `FOR UPDATE SKIP LOCKED`
- Configurable worker concurrency
- Continuous job polling
- Graceful worker shutdown

### Queue Management
- Project-based job queues
- Queue priority
- Queue concurrency limits
- Pause and resume queues
- Queue-specific execution control

### Reliability
- Configurable retry handling
- Retry count tracking
- Dead Letter Queue (DLQ)
- Requeue failed jobs from the DLQ
- Worker heartbeat monitoring
- Stale worker detection
- Recovery and requeue of abandoned jobs

### Monitoring
- Worker CPU and memory monitoring
- Worker heartbeat history
- Job execution history
- Execution time tracking
- Dashboard statistics
- Active worker monitoring

## Architecture

```text
React Frontend
      |
      v
FastAPI REST API
      |
      v
PostgreSQL Database
      |
      v
Distributed Worker Pool
      |
      +--> Worker Thread 1
      +--> Worker Thread 2
      +--> Worker Thread 3
```

Workers continuously poll PostgreSQL for available jobs.

Jobs are claimed atomically using:

```sql
FOR UPDATE SKIP LOCKED
```

This prevents multiple workers from executing the same job simultaneously.

## Job Lifecycle

```text
QUEUED
   |
   v
CLAIMED
   |
   v
RUNNING
   |
   +----------> COMPLETED
   |
   v
FAILED
   |
   +----------> RETRY
   |
   v
DEAD
   |
   v
DEAD LETTER QUEUE
   |
   v
REQUEUE
   |
   v
QUEUED
```

Jobs can also transition from `QUEUED` or `CLAIMED` to `CANCELLED`.

## Concurrency Control

The worker supports concurrent execution using a thread pool.

Example:

```text
Worker Concurrency = 3

Thread 1 ---> Job A
Thread 2 ---> Job B
Thread 3 ---> Job C
```

Queue-level concurrency limits are also enforced.

A queue configured with:

```text
Concurrency Limit = 1
```

executes jobs sequentially.

## Worker Heartbeats and Crash Recovery

Workers periodically send heartbeat information containing:

- CPU usage
- Memory usage
- Last heartbeat timestamp
- Worker health information

If a worker stops sending heartbeats, it is detected as stale.

Jobs claimed by stale workers can be recovered and requeued for execution by active workers.

## Retry and Dead Letter Queue

Failed jobs are retried according to their configured maximum retry count.

Example:

```text
Attempt 1 -> FAILED
Attempt 2 -> FAILED
Attempt 3 -> FAILED
             |
             v
      DEAD LETTER QUEUE
```

Dead jobs can be manually requeued using the DLQ API.

## Idempotency

Jobs can include an `idempotency_key`.

This prevents duplicate job creation when the same request is submitted multiple times.

Example:

```text
payment-test-001
```

Submitting another job with the same key returns the existing job instead of creating a duplicate.

## API Endpoints

### Jobs

```text
GET    /jobs/
POST   /jobs/
POST   /jobs/batch
PATCH  /jobs/{job_id}/cancel
```

### Projects

```text
GET    /projects/
POST   /projects/
```

### Queues

```text
GET    /queues/
POST   /queues/
PATCH  /queues/{queue_id}/pause
PATCH  /queues/{queue_id}/resume
```

### Workers

```text
GET /workers/
```

### Executions

```text
GET /executions/
```

### Dead Letter Queue

```text
GET   /dead-letter/
PATCH /dead-letter/{job_id}/requeue
```

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- TanStack Query

### Worker

- Python
- SQLAlchemy
- ThreadPoolExecutor
- psutil
- PostgreSQL

## Project Structure

```text
distributed-job-scheduler/
|
+-- backend/
|   +-- alembic/
|   +-- app/
|   |   +-- api/
|   |   +-- database/
|   |   +-- models/
|   |   +-- repositories/
|   |   +-- schemas/
|   |   +-- services/
|   +-- tests/
|
+-- frontend/
|   +-- src/
|       +-- api/
|       +-- components/
|       +-- pages/
|
+-- worker/
|   +-- app/
|   |   +-- executor.py
|   |   +-- heartbeat.py
|   |   +-- poller.py
|   |   +-- retry.py
|   |   +-- worker.py
|   +-- tests/
|
+-- docs/
+-- docker/
+-- README.md
```

## Running the Project

### Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

Windows:

```bash
.\.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python -m alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Worker

```bash
cd worker
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Start the worker:

```bash
python -m app.main
```

Multiple worker processes can be started to demonstrate distributed job execution.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs using Vite.

## Key Distributed Systems Concepts Demonstrated

- Distributed job processing
- Atomic job claiming
- Database row locking
- Concurrent execution
- Queue concurrency control
- Priority scheduling
- Retry mechanisms
- Dead-letter queues
- Idempotent job creation
- Worker heartbeat monitoring
- Stale worker detection
- Crash recovery
- Graceful shutdown
- Job state validation

## Project Status

Completed and functional.

The platform supports distributed workers, concurrent job execution, scheduling, recurring jobs, retries, dead-letter queue recovery, worker monitoring, crash recovery, and queue-level concurrency control.
