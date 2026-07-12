import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import Projects from "../pages/Projects";
import Queues from "../pages/Queues";
import Jobs from "../pages/Jobs";
import Workers from "../pages/Workers";
import Executions from "../pages/Executions";
import DeadLetterQueue from "../pages/DeadLetterQueue";
import NotFound from "../pages/NotFound";
import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "./ProtectedRoute";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/queues" element={<Queues />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/workers" element={<Workers />} />
          <Route path="/executions" element={<Executions />} />
          <Route path="/dlq" element={<DeadLetterQueue />} />
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
