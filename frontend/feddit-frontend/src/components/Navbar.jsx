import { Link, useNavigate } from "react-router-dom";
import { Zap, LogIn, UserPlus, LogOut } from "lucide-react";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <Link to="/" className="nav-logo">
        <Zap fill="currentColor" size={24} />
        <span>Feddit</span>
      </Link>

      <div className="nav-links">
        {token ? (
          <>
            <button onClick={handleLogout} className="nav-btn btn-outline" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <LogOut size={16} /> Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">
              <button className="nav-btn btn-outline" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <LogIn size={16} /> Login
              </button>
            </Link>
            <Link to="/register">
              <button className="nav-btn btn-solid" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <UserPlus size={16} /> Register
              </button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}