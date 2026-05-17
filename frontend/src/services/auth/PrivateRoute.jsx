import React from 'react';
import {Navigate, Outlet} from 'react-router-dom';

const PrivateRoute = ({ children, allowedRoles }) => {
    const token = localStorage.getItem("accessToken");
    const currentRole = localStorage.getItem("role");

    if (!token || !currentRole) {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("role");
        return <Navigate to="/login" replace />;
    }

    const hasAccess = allowedRoles.some(role =>
        currentRole.toUpperCase().includes(role.toUpperCase())
    );

    if (!hasAccess) {
        console.warn("Unauthorized! User role:", currentRole, "Required roles:", allowedRoles);
        if (currentRole.toUpperCase() === "ADMIN") return <Navigate to="/admin/dashboard" replace />;
        return <Navigate to="/" replace />;
    }

    return children ? children : <Outlet />;
};

export default PrivateRoute;
