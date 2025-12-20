import { formatPrice, translateAttributeName } from '../utils/helpers';
import './OrderModal.css';

export default function OrderModal({ order, products = [], onClose }) {

    useEffect(() => {
        const handleEsc = (e) => {
            if (e.key === 'Escape') onClose();
        };
        
        document.body.style.overflow = 'hidden';
        window.addEventListener('keydown', handleEsc);
        
        return () => {
            window.removeEventListener('keydown', handleEsc);
            document.body.style.overflow = 'unset';
        };
    }, [onClose]);

    if (!order) return null;

    // Функция для получения названия продукта по ID
    const getProductName = (productId) => {
        const product = products.find(p => p.product_id === productId);
        return product?.name || 'Продукт';
    };
    
    const calculateTotal = () => {
        return order.items.reduce((sum, item) => {
            // unit_price already includes all option prices from backend
            const itemTotal = item.unit_price * item.quantity;
            return sum + itemTotal;
        }, 0);
    };

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="order-modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={onClose} aria-label="Закрыть">
                    ✕
                </button>
                
                <div className="order-modal-body">
                    <h2 className="order-modal-title">Заказ #{order.order_id}</h2>
                    <p className="order-modal-date">
                        {new Date(order.created_at).toLocaleString('ru-RU', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                        })}
                    </p>

                    <div className="order-items-list">
                        {order.items.map((item, idx) => (
                            <div key={idx} className="order-item">
                                <div className="order-item-header">
                                    <span className="order-item-name">
                                        {getProductName(item.product_id)}
                                    </span>
                                    <span className="order-item-quantity">× {item.quantity}</span>
                                </div>
                                
                                {item.selected_options && item.selected_options.length > 0 && (
                                    <div className="order-item-options">
                                        {item.selected_options.map((opt, optIdx) => (
                                            <div key={optIdx} className="order-option">
                                                <span className="option-label">
                                                    {translateAttributeName(opt.attribute_type)}:
                                                </span>
                                                <span className="option-value">
                                                    {opt.value}
                                                    {opt.extra_price > 0 && 
                                                        ` (+${formatPrice(opt.extra_price)})`
                                                    }
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                )}

                                <div className="order-item-price">
                                    {formatPrice(item.unit_price * item.quantity)}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="order-modal-total">
                        <span>Итого:</span>
                        <span className="total-amount">{formatPrice(calculateTotal())}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
