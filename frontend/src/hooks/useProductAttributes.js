import { useState, useEffect, useMemo } from 'react';
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

    // Calculate initial selected options based on attributes
    const initialSelectedOptions = useMemo(() => {
        if (!attributes || attributes.length === 0) return {};
        
        const initial = {};
        attributes.forEach(attr => {
            if (attr.options && attr.options.length > 0) {
                initial[attr.attribute_type_id] = attr.options[0].option_id;
            }
        });
        return initial;
    }, [attributes]);

    return { attributes, loading, error, initialSelectedOptions };
}
