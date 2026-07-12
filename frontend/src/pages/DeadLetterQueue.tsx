import { useEffect, useState } from "react";
import api from "../api/axios";

interface DeadLetterJob {
  id: number;
  name: string;
  status: string;
  retry_count: number;
  max_retries: number;
}

export default function DeadLetterQueue() {
  const [jobs, setJobs] = useState<DeadLetterJob[]>([]);

  const loadJobs = async () => {
    try {
      const response = await api.get("/jobs/");
      const deadJobs = response.data.filter(
        (job: DeadLetterJob) => job.status === "DEAD"
      );

      setJobs(deadJobs);
    } catch (error) {
      console.error("Failed to load dead letter queue", error);
    }
  };

  useEffect(() => {
    loadJobs();
  }, []);

  return (
    <div className="page-container">
      <h1>Dead Letter Queue</h1>

      {jobs.length === 0 ? (
        <p>No dead letter jobs.</p>
      ) : (
        <div className="queue-list">
          {jobs.map((job) => (
            <div className="queue-card" key={job.id}>
              <h3>{job.name}</h3>
              <p>Status: {job.status}</p>
              <p>
                Retries: {job.retry_count} / {job.max_retries}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
