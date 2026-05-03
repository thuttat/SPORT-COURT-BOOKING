import {Button} from "../../components/common/Button.jsx";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {useAuth} from "../../services/auth/AuthContext.jsx";

export function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState("");
    const navigate = useNavigate();
    const {login} = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrorMsg("");
        if (!username || !password) {
            alert("Please enter your username and password!");
            return;
        }
        setLoading(true);
        try {
            const userData = await login(username, password);

            if (userData.role === "ADMIN") {
                navigate("/admin/dashboard");
            } else {
                navigate("/");
            }
        } catch (error) {
            setErrorMsg(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="login-container">
                <div className="card login-card">
                    <div className="login-header">
                        <div className="login-icon">
                            🔐
                        </div>

                        <h3>Welcome Back</h3>
                        <p className="text-muted">
                            Sign in to book your sports court
                        </p>
                    </div>

                    {errorMsg && (<p className="error">{errorMsg}</p>)}

                    <form className="login-form" onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>Username</label>
                            <input
                                type="text"
                                className="input"
                                placeholder="Enter your username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                className="input"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        <Button className="btn-primary" type="submit" disabled={loading}>
                            {loading ? "Signing in..." : "Sign In"}
                        </Button>
                    </form>

                    <div className="login-footer">
                        <p className="text-muted">
                            Don't have an account?{" "}
                            <a href="/register" className="link-primary">
                                Sign up
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}