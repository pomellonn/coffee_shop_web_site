import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthContext';

/**
 * Защищенный маршрут, который проверяет аутентификацию и роли.
 * @param {object} props
 * @param {string[]} [props.roles] 
 */
const ProtectedRoute = ({ roles }) => {
    const { isAuthenticated, role } = useAuth();

    if (!isAuthenticated) {

        return <Navigate to="/login" replace />;
    }


    if (roles && roles.length > 0 && !roles.includes(role)) {

        return <Navigate to="/403" replace />;
    }


    return <Outlet />;
};

export default ProtectedRoute;
