import { useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/", { replace: true });
  };

  return (
    <header className="navbar">
      <h2>Distributed Job Scheduler</h2>

      <button
        className="profile-button"
        onClick={handleLogout}
        title="Logout"
      >
        U
      </button>
    </header>
  );
}
