import { useState, useEffect } from 'react';
import api from '../api';

export function useProductAttributes(productId) {
    const [attributes, setAttributes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!productId) {
            setLoading(false);
            return;
        }

        const loadAttributes = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await api.get(`/products/${productId}/attributes`);
                setAttributes(response.data.attributes || []);
            } catch (err) {
                setError(err.response?.data?.detail || 'Не удалось загрузить опции продукта');
            } finally {
                setLoading(false);
            }
        };

        loadAttributes();
    }, [productId]);

    return { attributes, loading, error };
}
