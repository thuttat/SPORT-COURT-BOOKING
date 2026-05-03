import React, { createContext, useContext, useState } from "react";

const AuthContext = createContext();
const API_URL = "http://localhost:5000/api";

export function AuthProvider({ children }) {
    const [user, setUser] = useState(() => {
        const savedUser = localStorage.getItem("user");
        return savedUser ? JSON.parse(savedUser) : null;
    });

    const login = async (username, password) => {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            body: formData,
        })

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || "Invalid credentials!");
        }

        const userData = data.data;
        setUser(userData);
        localStorage.setItem("accessToken", "flask-session-active");
        localStorage.setItem("role", userData.role);
        localStorage.setItem("user", JSON.stringify(userData));

        return userData;
    };

    const register = async (fullname, username, email, password, confirm, avatarFile) => {
        const formData = new FormData();
        formData.append("fullname", fullname);
        formData.append("email", email);
        formData.append("username", username);
        formData.append("password", password);
        formData.append("confirm", confirm);
        formData.append("avatar", avatarFile);

        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || "Registration failed!");
        }
        return data;
    };

    const logout = async () => {
        try {
            await fetch(`${API_URL}/logout`, { method: "POST" });
        } catch (error) {
            console.error("Logout error", error);
        }
        setUser(null);
        localStorage.removeItem("accessToken");
        localStorage.removeItem("role");
        localStorage.removeItem("user");
    };

    const isAdmin = user?.role === "ADMIN";

    return (
        <AuthContext.Provider
            value={{
                user,
                login,
                register,
                logout,
                isAdmin
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }

    return context;
}