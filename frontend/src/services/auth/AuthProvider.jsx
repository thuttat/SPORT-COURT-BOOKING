import React, {useState} from "react";
import {AuthContext} from "./authContext.js";
import {loginRequest, logoutRequest, registerRequest} from "../apis.js";

export function AuthProvider({ children }) {
    const [user, setUser] = useState(() => {
        const savedUser = localStorage.getItem("user");
        return savedUser ? JSON.parse(savedUser) : null;
    });

    const login = async (username, password) => {
        try {
            const response = await loginRequest(username, password);
            const userData = response.data.data;

            setUser(userData);
            localStorage.setItem("accessToken", "flask-session-active");
            localStorage.setItem("role", userData.role);
            localStorage.setItem("user", JSON.stringify(userData));

            return userData;
        } catch (error) {
            const errorMsg = error.response?.data?.message || "Invalid credentials!";
            throw new Error(errorMsg);
        }
    };

    const register = async (fullname, username, email, password, confirm, avatarFile) => {
        try {
            const response = await registerRequest(fullname, username, email, password, confirm, avatarFile);
            return response.data;
        } catch (error) {
            const errorMsg = error.response?.data?.message || "Registration failed!";
            throw new Error(errorMsg);
        }
    };

    const logout = async () => {
        try {
            await logoutRequest();
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

