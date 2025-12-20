import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useCart } from '../services/CartContext';
import { formatPrice, translateAttributeName } from '../utils/helpers';
import './Cart.css';

export default function Cart() {
    const { cart, removeFromCart, updateQuantity, getCartTotal, getCartCount, submitOrder } = useCart();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [orderSuccess, setOrderSuccess] = useState(false);
    const [orderData, setOrderData] = useState(null);
    const navigate = useNavigate();
    const params = useParams();
    
    // Get shopId from cart items or params
    const shopId = params.shopId || (cart.length > 0 ? cart[0].shopId : null);

    const handleQuantityChange = (index, newQuantity) => {
        if (newQuantity <= 0) {
            if (window.confirm('Удалить товар из корзины?')) {
                removeFromCart(index);
            }
        } else {
            updateQuantity(index, newQuantity);
        }
    };

    const handleSubmitOrder = async () => {
        if (!shopId) {
            alert('Не указана кофейня для заказа');
            return;
        }

        if (cart.length === 0) {
            alert('Корзина пуста');
            return;
        }

        setIsSubmitting(true);
        try {
            await submitOrder(
                shopId,
                (data) => {
                    setOrderData(data);
                    setOrderSuccess(true);
                },
                (error) => {
                    console.error('Order submission error:', error);
                    alert(error.response?.data?.detail || 'Ошибка при создании заказа');
                }
            );
        } catch (error) {
            console.error('Order error:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    if (orderSuccess && orderData) {
        return (
            <div className="cart-container">
                <div className="order-success">
                    <div className="success-icon">✓</div>
                    <h2>Заказ успешно создан!</h2>
                    <p className="order-number">Номер заказа: <strong>#{orderData.order_id}</strong></p>
                    <p className="order-total">Сумма: <strong>{formatPrice(orderData.total_amount)}</strong></p>
                    <p className="order-date">
                        Дата: {new Date(orderData.created_at).toLocaleString('ru-RU')}
                    </p>
                    <div className="success-actions">
                        <button 
                            className="btn-primary" 
                            onClick={() => navigate('/orders')}
                        >
                            Мои заказы
                        </button>
                        <button 
                            className="btn-secondary" 
                            onClick={() => {
                                setOrderSuccess(false);
                                setOrderData(null);
                                navigate(`/menu/${shopId}`);
                            }}
                        >
                            Продолжить покупки
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    if (cart.length === 0) {
        return (
            <div className="cart-container">
                <div className="empty-cart">
                    <h2>Корзина пуста</h2>
                    <p>Добавьте товары из меню</p>
                    <button 
                        className="btn-primary" 
                        onClick={() => navigate('/menu')}
                    >
                        Перейти к меню
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="cart-container">
            <h1>Корзина</h1>
            
            <div className="cart-content">
                <div className="cart-items">
                    {cart.map((item, index) => {
                        const itemTotal = (item.unit_price + (item.selected_options || []).reduce(
                            (sum, opt) => sum + opt.extra_price, 0
                        )) * item.quantity;

                        return (
                            <div key={index} className="cart-item">
                                <div className="item-details">
                                    <h3>{item.product_name || `Продукт #${item.product_id}`}</h3>
                                    
                                    {item.selected_options && item.selected_options.length > 0 && (
                                        <div className="item-options">
                                            {item.selected_options.map((opt, idx) => (
                                                <span key={idx} className="option-tag">
                                                    {translateAttributeName(opt.attribute_type)}: {opt.value}
                                                    {opt.extra_price > 0 && ` (+${formatPrice(opt.extra_price)})`}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                    
                                    <div className="item-price">
                                        <span className="price-label">Цена за ед.:</span>
                                        <span className="price-value">{formatPrice(item.unit_price)}</span>
                                    </div>
                                </div>
                                
                                <div className="item-controls">
                                    <div className="quantity-controls">
                                        <button 
                                            className="qty-btn"
                                            onClick={() => handleQuantityChange(index, item.quantity - 1)}
                                        >
                                            −
                                        </button>
                                        <span className="qty-value">{item.quantity}</span>
                                        <button 
                                            className="qty-btn"
                                            onClick={() => handleQuantityChange(index, item.quantity + 1)}
                                        >
                                            +
                                        </button>
                                    </div>
                                    
                                    <div className="item-total">
                                        {formatPrice(itemTotal)}
                                    </div>
                                    
                                    <button 
                                        className="remove-btn"
                                        onClick={() => {
                                            if (window.confirm('Удалить товар из корзины?')) {
                                                removeFromCart(index);
                                            }
                                        }}
                                    >
                                        <span className="material-symbols-outlined">delete</span>
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
                
                <div className="cart-summary">
                    <h2>Итого</h2>
                    <div className="summary-row">
                        <span>Товаров:</span>
                        <span>{getCartCount()} шт.</span>
                    </div>
                    <div className="summary-row total">
                        <span>Итоговая сумма:</span>
                        <span className="total-price">{formatPrice(getCartTotal())}</span>
                    </div>
                    
                    <button 
                        className="submit-order-btn"
                        onClick={handleSubmitOrder}
                        disabled={isSubmitting || cart.length === 0}
                    >
                        {isSubmitting ? 'Оформление...' : 'Сделать заказ'}
                    </button>
                    
                    <button 
                        className="continue-shopping-btn"
                        onClick={() => navigate(`/menu/${shopId || ''}`)}
                    >
                        Продолжить покупки
                    </button>
                </div>
            </div>
        </div>
    );
}
