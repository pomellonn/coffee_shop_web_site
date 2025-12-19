import api from "../api";

export const getOneShopAnalytics = async (dateFrom, dateTo) => {
  const { data } = await api.get("manager/analytics/", {
    params: {
      date_from: dateFrom,
      date_to: dateTo,
    },
  });
  return data;
};

export const getAllProducts = async () => {
    const { data } = await api.get("/products/");
    return data;
};

export const getShopMenu = async () => {
    const { data } = await api.get("/manager/menu/");
    return data;    
};

export const addMenuItem = async (payload) => {
    const { data } = await api.post("/manager/menu/", payload);
    return data;
};

export const updateMenuItem = async (menuId, payload) => {
    const { data } = await api.put(`/manager/menu/${menuId}`, payload);
    return data;
};

export const deleteMenuItem = async (menuId) => {
    await api.delete(`/manager/menu/${menuId}`);
};


export const getOrdersCount = async (date) => {
    const params = {};
    if (date) params.target_date = date;
    const { data } = await api.get('/manager/orders/orders-count', { params });
    return data.count;
};

export const getShopInfo = async () => {
    const { data } = await api.get("/manager/shops/info");
    return data;
};

export const getTodayOrders = async () => {
    const { data } = await api.get("/manager/orders/today");
    return data;
};