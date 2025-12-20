import api from '../api';

export const getMyOrders = async () => {
    const response = await api.get('/orders/me');
    return response.data;
};

export const getOrderById = async (orderId) => {
    const response = await api.get(`/orders/${orderId}`);
    return response.data;
};
