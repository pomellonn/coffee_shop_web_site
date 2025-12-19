import React from 'react';
import { Outlet } from 'react-router-dom';
import { CartProvider } from '../services/CartContext';

export default function CustomerLayout() {
    return (
        <CartProvider>
            <Outlet />
        </CartProvider>
    );
}
