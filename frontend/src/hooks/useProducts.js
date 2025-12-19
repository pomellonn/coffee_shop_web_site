import { useState, useEffect } from 'react';
import api from '../api';

export const useFeaturedProducts = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await api.get('/products');
                const all = Array.isArray(response.data) ? response.data : [];
                const targets=['cacao', 'matcha', 'hotchoc' ]
                const found = targets.map(t => {
                    const low = t.toLowerCase();
                    return all.find(p => {
                        const name = (p.name || '').toLowerCase();
                        const slug = (p.slug || '').toLowerCase();
                        const img = (p.image_url || '').toLowerCase();
                        const id = String(p.product_id ?? p.id ?? '').toLowerCase();
                        return name.includes(low) || slug.includes(low) || img.includes(low) || id === low;
                    });
                }).filter(Boolean);
                setProducts(found.length ? found : all.slice(0, targets.length));

            } catch (err) {
                console.error('Ошибка загрузки продуктов:', err);
                setError(err.message || 'Ошибка загрузки продуктов');
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    return { products, loading, error };
};

/**
 * Хук для получения всех продуктов
 * @returns {Object} - { products, loading, error }
 */
export const useProducts = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await api.get('/products');
                setProducts(response.data);
            } catch (err) {
                console.error('Ошибка загрузки продуктов:', err);
                setError(err.message || 'Ошибка загрузки продуктов');
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    return { products, loading, error };
};

/**
 * Хук для получения конкретного продукта по ID
 * @param {number} productId - ID продукта
 * @returns {Object} - { product, loading, error }
 */
export const useProduct = (productId) => {
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!productId) {
            setLoading(false);
            return;
        }

        const fetchProduct = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await api.get(`/products/${productId}`);
                setProduct(response.data);
            } catch (err) {
                console.error('Ошибка загрузки продукта:', err);
                setError(err.message || 'Ошибка загрузки продукта');
            } finally {
                setLoading(false);
            }
        };

        fetchProduct();
    }, [productId]);

    return { product, loading, error };
};
