import React, {useEffect, useState} from "react";
import {AuthContext} from "./authContext.js";
import {getCurrentUserRequest, loginRequest, logoutRequest, registerRequest, updateProfileRequest} from "../apis.js";

export function AuthProvider({ children }) {
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(() => {
        const savedUser = localStorage.getItem("user");
        return savedUser ? JSON.parse(savedUser) : null;
    });

    const checkAuth = async () => {
        try {
            const res = await getCurrentUserRequest();
            const userData = res.data.data;

            setUser(userData);
            localStorage.setItem("role", userData.user_role);
            localStorage.setItem("user", JSON.stringify(userData));
        } catch (error) {
            setUser(null);
            localStorage.removeItem("role");
            localStorage.removeItem("user");
            localStorage.removeItem("accessToken");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        checkAuth();
    }, []);

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

    const updateProfile = async (formData) => {
        try {
            const response = await updateProfileRequest(formData);
            const updatedData = response.data.data;
            setUser(updatedData);
            localStorage.setItem("role", updatedData.user_role);
            localStorage.setItem("user", JSON.stringify(updatedData));

            return updatedData;
        } catch (error) {
            throw error;
        }
    };

    const isAdmin = user?.role === "ADMIN" || user?.user_role === "ADMIN";

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                register,
                logout,
                isAdmin,
                updateProfile,
                refreshUser: checkAuth,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

