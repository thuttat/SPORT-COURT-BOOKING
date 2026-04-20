import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../../services/auth/AuthContext.jsx";
import { Button } from "./Button.jsx";

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
                        You need to log in to the system to view your booking history and manage your personal profile.
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

    return <Outlet />;
}