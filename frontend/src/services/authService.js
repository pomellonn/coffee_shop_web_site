import api from '../api'
import { jwtDecode } from 'jwt-decode'; 

export const login = async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const { data } = await api.post('/auth/token', formData);
    console.log('[authService] Login response:', data);
    localStorage.setItem('access_token', data.access_token);
    return data;
};

export const logout = () => {
    localStorage.removeItem('access_token');
};

export const register = async (userData) => {
    const { data } = await api.post('/users/register', userData);
    console.log('[authService] Register response:', data);
    if (data.token && data.token.access_token) {
        localStorage.setItem('access_token', data.token.access_token);
        console.log('[authService] Token saved to localStorage');
    } else {
        console.error('[authService] No token in register response!');
    }
    return data;
}

export const getCurrentUser = async () => {

    const { data } = await api.get('/users/me');
    return data;
};



const decodeToken = (token) => {
    try {
        return jwtDecode(token);
    } catch (error) {
        console.error("Failed to decode token:", error);
        return null;
    }
};

export const getAuthDataFromStorage = () => {
    const token = localStorage.getItem('access_token');
    console.log('[authService] Getting auth data from storage, token:', token ? 'exists' : 'missing');
    
    if (token) {
        const decoded = decodeToken(token);
        console.log('[authService] Decoded token:', decoded);

        const role = decoded?.role;
        const authData = { isAuthenticated: true, role: role };
        console.log('[authService] Returning auth data:', authData);

        return authData;
    }
    console.log('[authService] No token, returning unauthenticated');
    return { isAuthenticated: false, role: null };
};