import { useEffect, useState } from "react";
import api from "../api/axios";
import "./Workers.css";

interface Worker {
  id: number;
  name: string;
  status: string;
  last_heartbeat: string | null;
}

export default function Workers() {
  const [workers, setWorkers] = useState<Worker[]>([]);

  const loadWorkers = async () => {
    try {
      const response = await api.get("/workers/");
      setWorkers(response.data);
    } catch (error) {
      console.error("Failed to load workers", error);
    }
  };

  useEffect(() => {
    loadWorkers();

    const interval = setInterval(loadWorkers, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="workers-page">
      <h1>Workers</h1>

      <div className="worker-list">
        {workers.map((worker) => (
          <div className="worker-card" key={worker.id}>
            <h3>{worker.name}</h3>
            <p>Worker ID: {worker.id}</p>
            <p>Status: {worker.status}</p>
            <p>
              Last Heartbeat: {" "}
              {worker.last_heartbeat
                ? new Date(worker.last_heartbeat).toLocaleString()
                : "N/A"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
