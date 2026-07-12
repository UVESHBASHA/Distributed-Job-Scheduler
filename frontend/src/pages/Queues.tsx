import { useEffect, useState } from "react";
import api from "../api/axios";
import "./Queues.css";

interface Queue {
  id: number;
  project_id: number;
  retry_policy_id: number | null;
  name: string;
  description: string | null;
  priority: number;
  concurrency_limit: number;
  is_paused: boolean;
}

interface Project {
  id: number;
  name: string;
}

export default function Queues() {
  const [queues, setQueues] = useState<Queue[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);

  const [projectId, setProjectId] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState(1);
  const [concurrencyLimit, setConcurrencyLimit] = useState(1);

  const loadData = async () => {
    try {
      const [queueResponse, projectResponse] = await Promise.all([
        api.get("/queues/"),
        api.get("/projects/"),
      ]);

      setQueues(queueResponse.data);
      setProjects(projectResponse.data);
    } catch (error) {
      console.error("Failed to load queues", error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const createQueue = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await api.post("/queues/", {
        project_id: Number(projectId),
        retry_policy_id: null,
        name,
        description,
        priority,
        concurrency_limit: concurrencyLimit,
      });

      setName("");
      setDescription("");
      setPriority(1);
      setConcurrencyLimit(1);

      await loadData();
    } catch (error) {
      console.error("Failed to create queue", error);
      alert("Failed to create queue");
    }
  };

  const toggleQueueStatus = async (queue: Queue) => {
    try {
      const endpoint = queue.is_paused
        ? `/queues/${queue.id}/resume`
        : `/queues/${queue.id}/pause`;

      await api.patch(endpoint);

      await loadData();
    } catch (error) {
      console.error("Failed to update queue status", error);
      alert("Failed to update queue status");
    }
  };

  return (
    <div className="queues-page">
      <h1>Queues</h1>

      <form className="queue-form" onSubmit={createQueue}>
        <select
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
          required
        >
          <option value="">Select Project</option>

          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Queue name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <input
          type="number"
          min="1"
          placeholder="Priority"
          value={priority}
          onChange={(e) => setPriority(Number(e.target.value))}
        />

        <input
          type="number"
          min="1"
          placeholder="Concurrency"
          value={concurrencyLimit}
          onChange={(e) => setConcurrencyLimit(Number(e.target.value))}
        />

        <button type="submit">Create Queue</button>
      </form>

      <div className="queue-list">
        {queues.map((queue) => (
          <div className="queue-card" key={queue.id}>
            <h3>{queue.name}</h3>

            <p>{queue.description || "No description"}</p>

            <div className="queue-details">
              <span>Priority: {queue.priority}</span>
              <span>Concurrency: {queue.concurrency_limit}</span>
            </div>

            <p>
              Status: {queue.is_paused ? "Paused" : "Active"}
            </p>

            <button
              type="button"
              onClick={() => toggleQueueStatus(queue)}
            >
              {queue.is_paused ? "Resume Queue" : "Pause Queue"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
