import { useEffect, useState } from "react";
import api from "../api/axios";
import "./Projects.css";

interface Project {
  id: number;
  name: string;
  description?: string;
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(true);

  const loadProjects = async () => {
    try {
      const response = await api.get("/projects/");
      setProjects(response.data);
    } catch (error) {
      console.error("Failed to load projects", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const createProject = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await api.post("/projects/", {
        name,
        description,
        organization_id: 1,
      });

      setName("");
      setDescription("");
      await loadProjects();
    } catch (error) {
      console.error("Failed to create project", error);
      alert("Failed to create project");
    }
  };

  return (
    <div className="projects-page">
      <div className="projects-header">
        <h1>Projects</h1>
      </div>

      <form className="project-form" onSubmit={createProject}>
        <input
          type="text"
          placeholder="Project name"
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

        <button type="submit">Create Project</button>
      </form>

      <div className="project-list">
        {loading ? (
          <p>Loading projects...</p>
        ) : projects.length === 0 ? (
          <p>No projects found.</p>
        ) : (
          projects.map((project) => (
            <div className="project-card" key={project.id}>
              <h3>{project.name}</h3>
              <p>{project.description || "No description"}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
