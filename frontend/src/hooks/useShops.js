import { useState, useEffect } from 'react';
import api from '../api';

/**
 * Хук для получения всех кофеен
 * @returns {Object} - { shops, loading, error }
 */
export const useShops = () => {
    const [shops, setShops] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchShops = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await api.get('/shops');
                setShops(response.data);
            } catch (err) {
                console.error('Ошибка загрузки кофеен:', err);
                setError(err.message || 'Ошибка загрузки кофеен');
            } finally {
                setLoading(false);
            }
        };

        fetchShops();
    }, []);

    return { shops, loading, error };
};

export const useShop = (shopId) => {
    const [shop, setShop] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!shopId) {
            setLoading(false);
            return;
        }

        const fetchShop = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await api.get(`/shops/${shopId}`);
                setShop(response.data);
            } catch (err) {
                console.error('Ошибка загрузки кофейни:', err);
                setError(err.message || 'Ошибка загрузки кофейни');
            } finally {
                setLoading(false);
            }
        };

        fetchShop();
    }, [shopId]);

    return { shop, loading, error };
};
