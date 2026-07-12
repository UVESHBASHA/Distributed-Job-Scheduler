import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute() {
  const token = localStorage.getItem("access_token");

  if (!token || token === "undefined") {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
