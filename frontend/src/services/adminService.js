import api from "../api";

// USERS
export const getUsers = async () => {
    const response = await api.get(`/admin/users/`);
    return response.data;
};
export const getManagers = async () => {
    const response = await api.get(`/admin/users/managers`);
    return response.data;
};
export const getCustomers = async () => {
    const response = await api.get(`/admin/users/customers`);
    return response.data;
};

export const createUser = async (userData) => {
    const response = await api.post(`/admin/users/`, userData);
    return response.data;
};

export const updateUser = async (userId, userData) => {
    const response = await api.put(`/admin/users/${userId}`, userData);
    return response.data;
};

export const deleteUser = async (userId) => {
    const response = await api.delete(`/admin/users/${userId}`);
    return response.data;
};

// PRODUCTS
export const getAllProducts = async () => {
    const response = await api.get(`/products/`);
    return response.data;
};

export const createProduct = async (productData) => {
    const response = await api.post(`/admin/products/`, productData);
    return response.data;
};

export const updateProduct = async (productId, productData) => {
    const response = await api.put(`/admin/products/${productId}`, productData);
    return response.data;
};

export const deleteProduct = async (productId) => {
    const response = await api.delete(`/admin/products/${productId}`);
    return response.data;
};

// SHOP MENU
export const getMenuItems = async () => {
    const response = await api.get(`/admin/menu/`);
    return response.data;
};

export const createMenuItem = async (menuData) => {
    const response = await api.post(`/admin/menu/`, menuData);
    return response.data;
};

export const updateMenuItemAdmin = async (menuId, menuData) => {
    const response = await api.put(`/admin/menu/${menuId}`, menuData);
    return response.data;
};

export const deleteMenuItemAdmin = async (menuId) => {
    const response = await api.delete(`/admin/menu/${menuId}`);
    return response.data;
};

// ANALYTICS 
export const getShopAnalytics = async (dateFrom, dateTo, shopId) => {
    const response = await api.get(`/admin/analytics/shops/one`, {
        params: {
            date_from: dateFrom, date_to: dateTo, shop_id: shopId
        }
    });
    return response.data;
};

export const getAllShopsAnalytics = async (dateFrom, dateTo) => {
    const response = await api.get(`/admin/analytics/shops/all`, {
        params: {
            date_from: dateFrom,
            date_to: dateTo,
        },
    });
    return response.data;
};

export const getTopClientsAnalytics = async (dateFrom, dateTo) => {
    const response = await api.get(`/admin/analytics/clients/top`, {
        params: {
            date_from: dateFrom,
            date_to: dateTo,
        },
    });
    return response.data;
};

export const getClientsStats = async (dateFrom, dateTo) => {
    const response = await api.get(`/admin/analytics/clients/stats`, {
        params: {
            date_from: dateFrom,
            date_to: dateTo,
        },
    });
    return response.data;
};

// ORDERS 
export const getOrders = async () => {
    const response = await api.get(`/admin/orders/`);
    return response.data;
};


// SHOPS
export const getAllShops = async () => {
    const response = await api.get(`/admin/shops/`);
    return response.data;
};


export const createShop = async (shopData) => {
    const response = await api.post(`/admin/shops/`, shopData);
    return response.data;
};


export const getShopAdmin = async (shopId) => {
    const response = await api.get(`/admin/shops/${shopId}`);
    return response.data;
};


export const updateShop = async (shopId, shopData) => {
    const response = await api.put(`/admin/shops/${shopId}`, shopData);
    return response.data;
};


export const deleteShop = async (shopId) => {
    const response = await api.delete(`/admin/shops/${shopId}`);
    return response.data;
};
