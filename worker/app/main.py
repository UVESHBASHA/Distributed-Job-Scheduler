import threading
import time
from concurrent.futures import ThreadPoolExecutor

from app.config import settings
from app.worker import register_worker
from app.heartbeat import start_heartbeat
from app.poller import claim_next_job
from app.executor import execute_job
from app.recovery import recover_stale_workers

MAX_CONCURRENT_JOBS = 3

def main():
    print("=" * 50)
    print("Distributed Job Scheduler Worker")
    print("=" * 50)

    worker_id = register_worker()

    print(f"Worker ID : {worker_id}")

    heartbeat_thread = threading.Thread(
        target=start_heartbeat,
        args=(
            worker_id,
            settings.HEARTBEAT_INTERVAL,
        ),
        daemon=True,
    )

    print("Heartbeat Started")
    heartbeat_thread.start()

    print(
        f"Worker polling started "
        f"(Concurrency={MAX_CONCURRENT_JOBS})"
    )

    executor = ThreadPoolExecutor(
        max_workers=MAX_CONCURRENT_JOBS
    )

    running_jobs = set()

    try:
        while True:
            completed_jobs = {
                future
                for future in running_jobs
                if future.done()
            }

            for future in completed_jobs:
                try:
                    future.result()
                except Exception as error:
                    print(
                        f"Execution Thread Error: {error}"
                    )

            running_jobs -= completed_jobs

            recover_stale_workers(stale_seconds=30)

            available_slots = (
                MAX_CONCURRENT_JOBS - len(running_jobs)
            )

            for _ in range(available_slots):
                job = claim_next_job(worker_id)

                if job is None:
                    break

                print(
                    f"Job Found: "
                    f"{job['id']} - {job['name']}"
                )

                future = executor.submit(
                    execute_job,
                    worker_id,
                    job,
                )

                running_jobs.add(future)

            if not running_jobs:
                print("No Jobs Available")

            time.sleep(settings.POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nWorker shutdown requested...")

    finally:
        print("Waiting for running jobs...")

        executor.shutdown(wait=True)

        print("Worker stopped safely")

if __name__ == "__main__":
    main()