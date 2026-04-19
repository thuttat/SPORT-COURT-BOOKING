import React, { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);

    const login = async (email, password) => {
        await new Promise(resolve => setTimeout(resolve, 500));

        if (email === "admin@sports.com") {
            setUser({
                id: "1",
                name: "Admin User",
                email: email,
                role: "admin"
            });
        } else {
            setUser({
                id: "2",
                name: email.split("@")[0],
                email: email,
                role: "user"
            });
        }
    };

    const register = async (name, email, password) => {
        await new Promise(resolve => setTimeout(resolve, 500));

        setUser({
            id: Date.now().toString(),
            name,
            email,
            role: "user"
        });
    };

    const logout = () => {
        setUser(null);
    };

    const isAdmin = user?.role === "admin";

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