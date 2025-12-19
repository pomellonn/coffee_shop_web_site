/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
    const [cart, setCart] = useState(() => {
        // Load cart from localStorage on init
        const savedCart = localStorage.getItem('cart');
        return savedCart ? JSON.parse(savedCart) : [];
    });
    const [pendingItem, setPendingItem] = useState(null);

    // Save cart to localStorage whenever it changes
    useEffect(() => {
        localStorage.setItem('cart', JSON.stringify(cart));
    }, [cart]);

    const addToCart = (item) => {
        setCart(prevCart => {
            const existingItemIndex = prevCart.findIndex(
                cartItem => 
                    cartItem.product_id === item.product_id && 
                    JSON.stringify(cartItem.option_ids) === JSON.stringify(item.option_ids)
            );

            if (existingItemIndex > -1) {
                // Update quantity if same product with same options exists
                const updatedCart = [...prevCart];
                updatedCart[existingItemIndex].quantity += item.quantity;
                return updatedCart;
            } else {
                // Add new item
                return [...prevCart, item];
            }
        });
    };

    const removeFromCart = (index) => {
        setCart(prevCart => prevCart.filter((_, i) => i !== index));
    };

    const clearCart = () => {
        setCart([]);
        localStorage.removeItem('cart');
    };

    const updateQuantity = (index, quantity) => {
        if (quantity <= 0) {
            removeFromCart(index);
            return;
        }
        setCart(prevCart => {
            const updatedCart = [...prevCart];
            updatedCart[index].quantity = quantity;
            return updatedCart;
        });
    };

    const submitOrder = async (shopId, onSuccess, onError) => {
        try {
            const orderData = {
                shop_id: shopId,
                items: cart
            };
            
            const response = await api.post('/orders/', orderData);
            clearCart();
            if (onSuccess) onSuccess(response.data);
            return response.data;
        } catch (error) {
            if (onError) onError(error);
            throw error;
        }
    };

    const getCartTotal = () => {
        return cart.reduce((total, item) => {
            const optionsPrice = (item.selected_options || []).reduce(
                (sum, opt) => sum + opt.extra_price, 0
            );
            return total + (item.unit_price + optionsPrice) * item.quantity;
        }, 0);
    };

    const getCartCount = () => {
        return cart.reduce((count, item) => count + item.quantity, 0);
    };

    return (
        <CartContext.Provider value={{ 
            cart, 
            addToCart, 
            removeFromCart, 
            clearCart, 
            updateQuantity,
            submitOrder,
            getCartTotal,
            getCartCount,
            pendingItem,
            setPendingItem
        }}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used within CartProvider');
    }
    return context;
};
