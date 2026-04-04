import { Link, useNavigate } from "react-router-dom";
import { Button } from "./Button.jsx";

export function Header() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("user");
        navigate("/login");
    };

    return (
        <header className="header">
            <div className="container header-inner">

                <Link to="/" className="logo">
                    <div className="logo-icon">📅</div>
                    <span className="logo-text">SportBook</span>
                </Link>

                <nav className="nav">
                    <Link to="/" className="nav-btn">Home</Link>
                    <Link to="/bookings" className="nav-btn">My Bookings</Link>
                    <Link to="/profile" className="nav-btn">Profile</Link>
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