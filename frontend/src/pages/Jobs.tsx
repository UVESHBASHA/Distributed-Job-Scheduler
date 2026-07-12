import { useEffect, useState } from "react";
import api from "../api/axios";
import "./Jobs.css";

interface Queue {
  id: number;
  name: string;
  is_paused: boolean;
}

interface Job {
  id: number;
  queue_id: number;
  name: string;
  job_type: string;
  status: string;
  priority: number;
  retry_count: number;
  max_retries: number;
}

export default function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [queues, setQueues] = useState<Queue[]>([]);

  const [queueId, setQueueId] = useState("");
  const [name, setName] = useState("");
  const [jobType, setJobType] = useState("IMMEDIATE");
  const [runAt, setRunAt] = useState("");
  const [cronExpression, setCronExpression] = useState("");
  const [priority, setPriority] = useState(1);
  const [maxRetries, setMaxRetries] = useState(3);
  const [payload, setPayload] = useState("{}");

  const loadData = async () => {
    try {
      const [jobResponse, queueResponse] = await Promise.all([
        api.get("/jobs/"),
        api.get("/queues/"),
      ]);

      setJobs(jobResponse.data);
      setQueues(queueResponse.data);
    } catch (error) {
      console.error("Failed to load jobs", error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const createJob = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      let parsedPayload = {};

      try {
        parsedPayload = JSON.parse(payload);
      } catch {
        alert("Payload must be valid JSON");
        return;
      }

      await api.post("/jobs/", {
        queue_id: Number(queueId),
        name,
        job_type: jobType,
        payload: parsedPayload,
        priority,
        run_at:
          jobType === "SCHEDULED" && runAt
            ? new Date(runAt).toISOString()
            : null,
        cron_expression:
          jobType === "RECURRING"
            ? cronExpression
            : null,
        max_retries: maxRetries,
      });

      setName("");
      setPayload("{}");
      setRunAt("");
      setCronExpression("");
      setPriority(1);
      setMaxRetries(3);

      await loadData();
    } catch (error) {
      console.error("Failed to create job", error);
      alert("Failed to create job");
    }
  };

  return (
    <div className="jobs-page">
      <h1>Jobs</h1>

      <form className="job-form" onSubmit={createJob}>
        <select
          value={queueId}
          onChange={(e) => setQueueId(e.target.value)}
          required
        >
          <option value="">Select Queue</option>

          {queues.map((queue) => (
            <option key={queue.id} value={queue.id}>
              {queue.name}
              {queue.is_paused ? " (Paused)" : ""}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Job name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <select
          value={jobType}
          onChange={(e) => setJobType(e.target.value)}
        >
          <option value="IMMEDIATE">Immediate</option>
          <option value="SCHEDULED">Scheduled</option>
          <option value="RECURRING">Recurring</option>
        </select>

        {jobType === "SCHEDULED" && (
          <input
            type="datetime-local"
            value={runAt}
            onChange={(e) => setRunAt(e.target.value)}
            required
          />
        )}

        {jobType === "RECURRING" && (
          <input
            type="text"
            placeholder="Cron expression e.g. */1 * * * *"
            value={cronExpression}
            onChange={(e) => setCronExpression(e.target.value)}
            required
          />
        )}

        <input
          type="number"
          min="1"
          placeholder="Priority"
          value={priority}
          onChange={(e) => setPriority(Number(e.target.value))}
        />

        <input
          type="number"
          min="0"
          placeholder="Max retries"
          value={maxRetries}
          onChange={(e) => setMaxRetries(Number(e.target.value))}
        />

        <textarea
          placeholder='Payload JSON: {"email":"test@example.com"}'
          value={payload}
          onChange={(e) => setPayload(e.target.value)}
        />

        <button type="submit">Create Job</button>
      </form>

      <div className="job-list">
        {jobs.map((job) => (
          <div className="job-card" key={job.id}>
            <h3>{job.name}</h3>

            <p>Type: {job.job_type}</p>
            <p>Status: {job.status}</p>
            <p>Priority: {job.priority}</p>

            <p>
              Retries: {job.retry_count} / {job.max_retries}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
