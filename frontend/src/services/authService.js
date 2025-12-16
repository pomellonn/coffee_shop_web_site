import api from '../api'
import { jwtDecode } from 'jwt-decode'; 

export const login = async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const { data } = await api.post('/auth/token', formData);
    localStorage.setItem('access_token', data.access_token);
    return data;
};

export const logout = () => {
    localStorage.removeItem('access_token');
};

export const register = async (userData) => {
    const { data } = await api.post('/users/register', userData);
    if (data.token && data.token.access_token) {
        localStorage.setItem('access_token', data.token.access_token);
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
    if (token) {
        const decoded = decodeToken(token);

        const role = decoded?.role;

        return { isAuthenticated: true, role: role };
    }
    return { isAuthenticated: false, role: null };
};