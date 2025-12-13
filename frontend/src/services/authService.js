import api from '../api'

export const login = async (email, password) =>{
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const {data} = await api.post('/auth/token', formData);
    localStorage.setItem('access_token', data.access_token);
    return data;
};

export const logout=()=>{
    localStorage.removeItem('access_token');
};

export const register = async (userData)=>{
    const {data} = await api.post('/users/register', userData);
    if (data.token && data.token.access_token){
        localStorage.setItem('access_token', data.token.access_token);
    }
    return data;
}

export const getCurrentUser = async () => {

  const { data } = await api.get('/users/me');
  return data;
};