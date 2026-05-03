import {Button} from "../../components/common/Button.jsx";
import {useNavigate} from "react-router-dom";
import {useAuth} from "../../services/auth/AuthContext.jsx";
import {useState} from "react";

export function Register() {
    const [fullname, setFullname] = useState("");
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [avatar, setAvatar] = useState(null);
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState({ text: "", isError: false });

    const navigate = useNavigate();
    const {register} = useAuth();
    const handleSubmit = async (e) => {
        e.preventDefault();
        setMsg({text: "", isError: false});

        if (password !== "" && password !== confirm) {
            setMsg({text: "Password do not match!", isError: true});
            return;
        }

        if (!avatar) {
            setMsg({ text: "Please upload an avatar!", isError: true });
            return;
        }
        setLoading(true);
        try {
            await register(fullname, username, email, password, confirm, avatar);
            setMsg({ text: "Register successfully!", isError: false});
            setTimeout(() => navigate("/login"), 1500);
        } catch (error) {
            setMsg({text: error.message, isError: true});
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
                            ✍️
                        </div>

                        <h3>Create Account</h3>
                        <p className="text-muted">
                            Join us to start booking
                        </p>
                    </div>

                    {msg.text && (<p className="error">{msg.text}</p>)}

                    <form className="login-form" onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>Full name</label>
                            <input
                                type="text"
                                className="input"
                                placeholder="Enter your full name"
                                required value={fullname}
                                onChange={(e) => setFullname(e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>Username</label>
                            <input
                                type="text"
                                className="input"
                                placeholder="Enter your username"
                            required value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>Email</label>
                            <input
                                type="email"
                                className="input"
                                placeholder="you@example.com"
                                required value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                className="input"
                                placeholder="Enter your password (min 8 chars, 1 special)"
                                required value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>Confirm password</label>
                            <input
                                type="password"
                                className="input"
                                placeholder="Confirm your password"
                                required value={confirm}
                                onChange={(e) => setConfirm(e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label>Avatar</label>
                            <input
                                type="file"
                                className="input"
                                accept="image/png, image/jpeg, image/jpg"
                                required
                                onChange={(e) => setAvatar(e.target.files[0])}
                                style={{ padding: '7px 14px' }}
                            />
                        </div>

                        <Button className="btn-primary" type="submit" disabled={loading}>
                            {loading ? "Signing Up..." : "Sign Up"}
                        </Button>
                    </form>

                    <div className="login-footer">
                        <p className="text-muted">
                            Already have an account?{" "}
                            <a href="/login" className="link-primary">
                                Sign in
                            </a>
                        </p>
                    </div>

                </div>
            </div>
        </div>
    );
}