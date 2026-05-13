import {useContext} from "react";

import {AuthContext} from "./authContext.js";

export const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }

    const isAuthorized = (requiredRole) => {
        return context.user && context.user.role === requiredRole;
    };

    return { ...context, isAuthorized };
}