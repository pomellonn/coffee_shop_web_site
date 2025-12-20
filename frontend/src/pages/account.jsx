import { useEffect, useState } from 'react';
import { useAuth } from '../services/AuthContext';
import { getMyOrders } from '../services/orderService';
import { getCurrentUser } from '../services/authService';
import OrderModal from '../components/OrderModal';
import { formatPrice } from '../utils/helpers';
import { useProducts } from '../hooks/useProducts';
import './Account.css';

export default function Account() {
    const { logout } = useAuth();
    const [user, setUser] = useState(null);
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedOrder, setSelectedOrder] = useState(null);
    const { products } = useProducts();

    useEffect(() => {
        fetchUserData();
    }, []);

    const fetchUserData = async () => {
        try {
            setLoading(true);
            const userData = await getCurrentUser();
            setUser(userData);
            
            const ordersData = await getMyOrders();
            setOrders(ordersData);
        } catch (error) {
            console.error('Ошибка при загрузке данных:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        if (window.confirm('Вы уверены, что хотите выйти?')) {
            logout();
            window.location.href = '/';
        }
    };


    const handleOrderClick = (order) => {
        setSelectedOrder(order);
    };

    if (loading) {
        return (
            <div className="account-container">
                <div className="loading">Загрузка...</div>
            </div>
        );
    }

    return (
        <div className="account-container">
            <div className="account-content">
                <div className="account-sidebar">
                    <div className="profile-section">
                        <div className="photo-upload-container">
                            <div className="photo-circle">
                                <div className="photo-placeholder">
                                    {user?.name?.charAt(0).toUpperCase() || '?'}
                                </div>
                            </div>
                        </div>
                        
                        <h2 className="user-name">{user?.name || 'Пользователь'}</h2>
                        <p className="user-email">{user?.email || ''}</p>
                    </div>

                    <button onClick={handleLogout} className="logout-button">
                        Выйти из аккаунта
                    </button>
                </div>

                <div className="account-main">
                    <h1 className="section-title">История заказов</h1>
                    
                    {orders.length === 0 ? (
                        <div className="no-orders">
                            <p>У вас пока нет заказов</p>
                        </div>
                    ) : (
                        <div className="orders-list">
                            {orders.map((order) => (
                                <div
                                    key={order.order_id}
                                    className="order-card"
                                    onClick={() => handleOrderClick(order)}
                                >
                                    <div className="order-header">
                                        <span className="order-number">Заказ #{order.order_id}</span>
                                        <span className="order-date">
                                            {new Date(order.created_at).toLocaleDateString('ru-RU', {
                                                day: '2-digit',
                                                month: '2-digit',
                                                year: 'numeric'
                                            })}
                                        </span>
                                    </div>
                                    <div className="order-info">
                                        <span className="order-items-count">
                                            Позиций: {order.items?.length || 0}
                                        </span>
                                        <span className="order-total">
                                            {formatPrice(
                                                order.items?.reduce((sum, item) => {
                                                    // unit_price already includes all option prices from backend
                                                    return sum + (item.unit_price * item.quantity);
                                                }, 0) || 0
                                            )}
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {selectedOrder && (
                <OrderModal
                    order={selectedOrder}
                    products={products}
                    onClose={() => setSelectedOrder(null)}
                />
            )}
        </div>
    );
}