import {NavLink, useNavigate} from "react-router-dom";
import { Button } from "./Button.jsx";
import {Calendar, House, LayoutDashboard, MapPin, UserPen} from "lucide-react";
import {useAuth} from "../../services/auth/AuthContext.jsx";
import "../styles/header.css"

export function Header() {
    const navigate = useNavigate();

    const {user, logout, isAdmin} = useAuth();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <header className="header">
            <div className="container header-inner">
                <NavLink to={isAdmin ? "/admin/dashboard" : "/"} className="logo">
                    <div className="logo-icon">📅</div>
                    <div className="logo-text-wrapper">
                        <span className="logo-text">SportBook</span>
                        {isAdmin && <span className="logo-admin-text">Admin Panel</span>}
                    </div>
                </NavLink>

                <nav className="nav">
                    {isAdmin ? (
                        <>
                            <NavLink to="/admin/dashboard" className={({ isActive }) =>
                                isActive ? "nav-btn active" : "nav-btn"
                            }><LayoutDashboard size={20} strokeWidth={1.75} /> Dashboard</NavLink>
                            <NavLink to="/admin/courts" className={({ isActive }) =>
                                isActive ? "nav-btn active" : "nav-btn"
                            }><MapPin size={20} strokeWidth={1.75} /> Courts</NavLink>
                            <NavLink to="/admin/bookings" className={({ isActive }) =>
                                isActive ? "nav-btn active" : "nav-btn"
                            }><Calendar size={20} strokeWidth={1.75} /> Bookings</NavLink>
                        </>
                    ) : (
                        <>
                            <NavLink to="/" className={({ isActive }) =>
                                isActive ? "nav-btn active" : "nav-btn"
                            }><House size={20} strokeWidth={1.75} /> Home</NavLink>
                            <NavLink to="/bookings" className={({ isActive }) =>
                                isActive ? "nav-btn active" : "nav-btn"
                            }><Calendar size={20} strokeWidth={1.75} /> My Bookings</NavLink>
                            <NavLink to="/profile" className={({ isActive }) =>
                                isActive ? "nav-btn active" : "nav-btn"
                            }><UserPen size={20} strokeWidth={1.75} /> Profile</NavLink>
                        </>
                    )}
                </nav>

                <div className="user-section">
                    {user ? (
                        <>
                            <div className="user-info">
                                <div className="user-name">{user.name}</div>
                                <div className="text-muted small">{user.email}</div>
                            </div>
                            <Button className="btn-danger" onClick={handleLogout}>
                                Log out
                            </Button>
                        </>
                    ) : (
                        <Button className="btn-primary" onClick={() => navigate("/login")}>
                            Log in
                        </Button>
                    )}
                </div>
            </div>
        </header>
    );
}