
import React, { createContext, useContext, useState } from 'react';
import { getAuthDataFromStorage, logout as apiLogout, login as apiLogin } from './authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [authData, setAuthData] = useState(getAuthDataFromStorage());
    const [loading, setLoading] = useState(false);

    const login = async (email, password) => {
        setLoading(true);
        try {
            await apiLogin(email, password);
            setAuthData(getAuthDataFromStorage());
            setLoading(false);
            return true;
        } catch (error) {
            setLoading(false);
            throw error;
        }
    };

    const logout = () => {
        apiLogout();
        setAuthData({ isAuthenticated: false, role: null });
    };

    return (
        <AuthContext.Provider value={{ ...authData, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);