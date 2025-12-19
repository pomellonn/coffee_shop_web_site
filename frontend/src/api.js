import axios from 'axios'

const API_URL = "https://localhost/api/v1/";
export const api=axios.create({baseURL: API_URL})

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;