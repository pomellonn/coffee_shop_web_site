import axios from 'axios'

// Prefer build-time `VITE_API_URL`, otherwise use relative API path so
// the browser uses the same origin (works with HTTPS termination).
const API_URL = import.meta.env.VITE_API_URL || '/api/v1/';
export const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;