import {Navigate, Outlet, useNavigate} from "react-router-dom";
import { Button } from "./Button.jsx";
import {useAuth} from "../../services/auth/useAuth.js";

export function ProtectedRoute() {
    const { user } = useAuth();
    const navigate = useNavigate();

    if (!user) {
        return (
            <div className="container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
                <div className="empty-state" style={{ padding: '40px', maxWidth: '450px', width: '100%', background: 'var(--card)' }}>
                    <div className="empty-icon" style={{ fontSize: '56px', marginBottom: '16px' }}>🔒</div>
                    <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '8px' }}>
                        Requires login
                    </h3>
                    <p className="text-muted" style={{ marginBottom: '24px' }}>
                        You need to log in to the system to booking sport court, view your booking history and manage your personal profile.
                    </p>
                    <Button
                        className="btn-primary"
                        style={{ width: '100%' }}
                        onClick={() => navigate("/login")}
                    >
                        Go to the Login page
                    </Button>
                </div>
            </div>
        );
    }

    if (user.role === "ADMIN") {
        return <Navigate to="/admin/dashboard" replace />;
    }

    return <Outlet />;
}