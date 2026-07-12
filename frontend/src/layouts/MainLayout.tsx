import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function MainLayout() {
  return (
    <div className="flex">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <Navbar />

        <main className="bg-slate-100 flex-1 p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
