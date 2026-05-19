import React, { useState, useEffect } from "react";
import {PageHeader} from "../../../components/common/PageHeader.jsx";
import { Card } from "../../../components/common/Card.jsx";
import { Button } from "../../../components/common/Button.jsx";
import { Badge } from "../../../components/common/Badge.jsx";
import { useAuth } from "../../../services/auth/useAuth.js";
import "./profile.css";

export function Profile() {
    const { user, loading, updateProfile } = useAuth();
    const [saving, setSaving] = useState(false);

    const [formData, setFormData] = useState({
        fullname: "",
        email: "",
        password: "",
        confirmPassword: ""
    });
    const [avatarFile, setAvatarFile] = useState(null);
    const [avatarPreview, setAvatarPreview] = useState(null);

    useEffect(() => {
        if (user) {
            setFormData(prev => ({
                ...prev,
                fullname: user.fullname || "",
                email: user.email || ""
            }));
            setAvatarPreview(user.avatar);
        }
    }, [user]);

    const handleAvatarChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setAvatarFile(file);
            setAvatarPreview(URL.createObjectURL(file));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (formData.password && formData.password !== formData.confirmPassword) {
            alert("Confirmed password doesn't match!");
            return;
        }
        setSaving(true);
        const payload = new FormData();

        if (formData.fullname) payload.append("fullname", formData.fullname);
        if (formData.email) payload.append("email", formData.email);
        if (formData.password) payload.append("password", formData.password);
        if (avatarFile) payload.append("avatar", avatarFile);

        try {
            await updateProfile(payload);
            alert("Update profile successfully!");
            setFormData(prev => ({ ...prev, password: "", confirmPassword: "" }));
            setAvatarFile(null);
        } catch (error) {
            alert(`Error: ${error.response?.data?.message}`);
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <div className="container loading">Loading...</div>;
    }

    return (
        <div className="container">
            <PageHeader header="Profile" text="Manage your account and preferences" />

            <div className="profile-layout">
                <Card className="profile-card">
                    <form onSubmit={handleSubmit}>
                        <div className="profile-avatar-section">
                            <div className="profile-avatar-container">
                                {avatarPreview ? (
                                    <img src={avatarPreview} alt="Avatar" className="profile-avatar-img" />
                                ) : (
                                    <div className="profile-avatar-placeholder">👤</div>
                                )}
                            </div>

                            <div className="profile-user-info">
                                <h3 className="profile-username">@{user?.username}</h3>
                                <div>
                                    <Badge variant={user?.user_role === "ADMIN" ? "danger" : "primary"}>
                                        {user?.user_role}
                                    </Badge>
                                </div>
                                <div className="profile-avatar-upload">
                                    <label className="profile-upload-label">
                                        <span className="profile-upload-text">Change profile avatar</span>
                                        <input
                                            type="file"
                                            accept="image/png, image/jpeg, image/jpg"
                                            onChange={handleAvatarChange}
                                            className="profile-upload-input"
                                        />
                                    </label>
                                </div>
                            </div>
                        </div>

                        <h4 className="profile-section-title">Information</h4>
                        <div className="profile-info-grid">
                            <div>
                                <label className="form-label">Full name</label>
                                <input
                                    type="text"
                                    className="input profile-input-field"
                                    value={formData.fullname}
                                    onChange={(e) => setFormData({ ...formData, fullname: e.target.value })}
                                    required
                                />
                            </div>
                            <div>
                                <label className="form-label">Email</label>
                                <input
                                    type="email"
                                    className="input profile-input-field"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    required
                                />
                            </div>
                        </div>

                        <h4 className="profile-section-title">Change password</h4>
                        <p className="profile-section-description">Leave this blank if you do not wish to change your current password.</p>
                        <div className="profile-password-grid">
                            <div>
                                <label className="form-label">New password</label>
                                <input
                                    type="password"
                                    className="input profile-input-field"
                                    placeholder="Enter new password..."
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="form-label">Confirm password</label>
                                <input
                                    type="password"
                                    className="input profile-input-field"
                                    placeholder="Enter confirm password..."
                                    value={formData.confirmPassword}
                                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                                />
                            </div>
                        </div>

                        <div className="form-actions profile-form-actions">
                            <Button type="submit" className="btn-primary profile-save-btn" disabled={saving}>
                                {saving ? "Saving..." : "Save change"}
                            </Button>
                        </div>
                    </form>
                </Card>

                <Card className="profile-terms-card">
                    <div style={{ borderBottom: '1px solid var(--border)', paddingBottom: '2px', marginBottom: '-22px' }}>
                        <h3>📄 Terms & Booking Policies</h3>
                    </div>

                    <div style={{ fontSize: '14px', lineHeight: '1.8' }}>
                        <p>By using our system, you agree to comply with the following regulations to ensure fairness for all players:</p>

                        <ul>
                            <li>
                                <strong>Minimum Duration:</strong> Each court booking must be at least <strong>1 hour</strong> long.
                            </li>
                            <li>
                                <strong>Daily Limit:</strong> A single account can book a maximum of <strong>3 courts per day</strong>.
                            </li>
                            <li>
                                <strong>Cancellation Deadline:</strong> You cannot cancel a booking if the start time is less than <strong>2 hours</strong> away.
                            </li>
                            <li className="cancel-rule">
                                <strong style={{ color: 'var(-destructive)' }}>⚠️ Cancellation Penalty Rule:</strong><br />
                                If you cancel <strong>three or more bookings within the last seven days (168 hours)</strong>, your account will be temporarily locked from booking. The system will automatically unlock it after <strong>7 days</strong> from the date of the first cancellation in that series of three violations.
                            </li>
                        </ul>
                    </div>
                </Card>
            </div>
        </div>
    );
}