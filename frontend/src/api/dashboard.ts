import api from "./axios";

export async function getDashboardStats() {
  const [jobs, workers, projects, queues] = await Promise.all([
    api.get("/jobs/"),
    api.get("/workers/"),
    api.get("/projects/"),
    api.get("/queues/"),
  ]);

  const now = new Date().getTime();

  const activeWorkers = workers.data.filter((worker: any) => {
    if (!worker.last_heartbeat) return false;

    const heartbeat = new Date(worker.last_heartbeat).getTime();

    return now - heartbeat < 60000;
  });

  return {
    jobs: jobs.data.length,
    workers: activeWorkers.length,
    projects: projects.data.length,
    queues: queues.data.length,
  };
}
