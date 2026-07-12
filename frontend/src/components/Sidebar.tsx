import {
  LayoutDashboard,
  FolderKanban,
  ListOrdered,
  Briefcase,
  Cpu,
  History,
  Trash2,
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";

const menu = [
  { name: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
  { name: "Projects", icon: FolderKanban, path: "/projects" },
  { name: "Queues", icon: ListOrdered, path: "/queues" },
  { name: "Jobs", icon: Briefcase, path: "/jobs" },
  { name: "Workers", icon: Cpu, path: "/workers" },
  { name: "Executions", icon: History, path: "/executions" },
  { name: "Dead Letter Queue", icon: Trash2, path: "/dlq" },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 h-screen bg-slate-900 text-white flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-xl font-bold">Scheduler</h1>
        <p className="text-sm text-slate-400 mt-1">Distributed Job Scheduler</p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menu.map((item) => {
          const Icon = item.icon;
          const active = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                active
                  ? "bg-blue-600 text-white"
                  : "hover:bg-slate-800 text-slate-300"
              }`}
            >
              <Icon size={20} />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
