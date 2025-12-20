import api from '../api';

/**
 * Shared service for common product operations
 */

/**
 * Get all products (used by both admin and manager)
 * @returns {Promise} Products array
 */
export const getAllProducts = async () => {
    const response = await api.get('/products/');
    return response.data;
};
