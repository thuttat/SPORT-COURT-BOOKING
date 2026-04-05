import {NavLink, useNavigate} from "react-router-dom";
import { Button } from "./Button.jsx";
import {Calendar, House, UserPen} from "lucide-react";

export function Header() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("user");
        navigate("/login");
    };

    return (
        <header className="header">
            <div className="container header-inner">
                <NavLink to="/" className="logo">
                    <div className="logo-icon">📅</div>
                    <span className="logo-text">SportBook</span>
                </NavLink>

                <nav className="nav">
                    <NavLink to="/" className={({ isActive }) =>
                        isActive ? "nav-btn active" : "nav-btn"
                    }><House size={20} strokeWidth={1.75} /> Home</NavLink>
                    <NavLink to="/bookings" className={({ isActive }) =>
                        isActive ? "nav-btn active" : "nav-btn"
                    }><Calendar size={20} strokeWidth={1.75} /> My Bookings</NavLink>
                    <NavLink to="/profile" className={({ isActive }) =>
                        isActive ? "nav-btn active" : "nav-btn"
                    }><UserPen size={20} strokeWidth={1.75} /> Profile</NavLink>
                </nav>

                <div className="user-section">
                    <div className="user-info">
                        <div className="user-name">John Doe</div>
                        <div className="text-muted small">john@example.com</div>
                    </div>

                    <Button className="btn-danger" onClick={handleLogout}>
                        Log out
                    </Button>
                </div>
            </div>
        </header>
    );
}