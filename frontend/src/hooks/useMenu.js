import { useState, useEffect } from 'react';
import api from '../api';

//хук для получения меню конкретной кофейни
export const useShopMenu = (shopId) => {
    const [menuItems, setMenuItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!shopId) {
            setLoading(false);
            return;
        }

        const fetchMenu = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await api.get(`/menu/${shopId}`);
                setMenuItems(response.data);
            } catch (err) {
                console.error('Ошибка загрузки меню:', err);
                setError(err.message || 'Ошибка загрузки меню');
            } finally {
                setLoading(false);
            }
        };

        fetchMenu();
    }, [shopId]);

    return { menuItems, loading, error };
};


export const useShopMenuSorted = (shopId, sortBy = 'name', order = 'asc') => {
    const [menuItems, setMenuItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!shopId) {
            setLoading(false);
            return;
        }

        const fetchMenu = async () => {
            try {
                setLoading(true);
                setError(null);
                
                let endpoint = `/menu/${shopId}`;
                if (sortBy === 'price' && order === 'asc') {
                    endpoint = `/menu/${shopId}/sorted-price-asc`;
                } else if (sortBy === 'price' && order === 'desc') {
                    endpoint = `/menu/${shopId}/sorted-price-desc`;
                } else if (sortBy === 'name' && order === 'asc') {
                    endpoint = `/menu/${shopId}/sorted-name-asc`;
                }
                
                const response = await api.get(endpoint);
                setMenuItems(response.data);
            } catch (err) {
                console.error('Ошибка загрузки меню:', err);
                setError(err.message || 'Ошибка загрузки меню');
            } finally {
                setLoading(false);
            }
        };

        fetchMenu();
    }, [shopId, sortBy, order]);

    return { menuItems, loading, error };
};
