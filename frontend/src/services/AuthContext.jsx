/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { getAuthDataFromStorage, logout as apiLogout, login as apiLogin } from './authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [authData, setAuthData] = useState(getAuthDataFromStorage());
    const [loading, setLoading] = useState(false);

    // Log auth state changes for debugging
    useEffect(() => {
        console.log('[AuthContext] Auth state updated:', authData);
    }, [authData]);

    const login = async (email, password) => {
        setLoading(true);
        try {
            await apiLogin(email, password);
            const newAuthData = getAuthDataFromStorage();
            console.log('[AuthContext] Login successful, new auth data:', newAuthData);
            setAuthData(newAuthData);
            setLoading(false);
            return true;
        } catch (error) {
            console.error('[AuthContext] Login failed:', error);
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