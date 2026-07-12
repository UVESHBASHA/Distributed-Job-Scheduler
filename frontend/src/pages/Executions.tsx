import { useEffect, useState } from "react";
import api from "../api/axios";
import "./Executions.css";

interface Execution {
  id: number;
  job_id: number;
  worker_id: number;
  status: string;
  execution_time_ms: number;
  job_name: string;
}

export default function Executions() {
  const [executions, setExecutions] = useState<Execution[]>([]);

  const loadExecutions = async () => {
    try {
      const response = await api.get("/executions/");
      setExecutions(response.data);
    } catch (error) {
      console.error("Failed to load executions", error);
    }
  };

  useEffect(() => {
    loadExecutions();
  }, []);

  return (
    <div className="executions-page">
      <h1>Executions</h1>

      {executions.length === 0 ? (
        <p>No execution history available.</p>
      ) : (
        <div className="execution-list">
          {executions.map((execution) => (
            <div className="execution-card" key={execution.id}>
              <h3>{execution.job_name}</h3>

              <p>Job ID: {execution.job_id}</p>
              <p>Worker ID: {execution.worker_id}</p>
              <p>Status: {execution.status}</p>
              <p>
                Execution Time: {execution.execution_time_ms} ms
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
