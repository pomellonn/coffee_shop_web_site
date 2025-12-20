import { formatPrice, translateAttributeName } from '../utils/helpers';
import { useModal } from '../hooks/useModal';
import { calculateItemTotal } from '../utils/priceCalculators';
import './OrderModal.css';

export default function OrderModal({ order, products = [], onClose }) {
    // Use modal hook for ESC and body scroll
    useModal(onClose);

    if (!order) return null;

    
    const calculateTotal = () => {
        return order.items.reduce((sum, item) => sum + calculateItemTotal(item), 0);
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
                                        {item.product?.name || 'Продукт'}
                                    </span>
                                    <span className="order-item-quantity">× {item.quantity}</span>
                                </div>
                                
                                {item.attributes && item.attributes.length > 0 && (
                                    <div className="order-item-options">
                                        {item.attributes.map((attr, attrIdx) => (
                                            <div key={attrIdx} className="order-option">
                                                <span className="option-label">
                                                    {attr.option?.attribute_type?.name}:
                                                </span>
                                                <span className="option-value">
                                                    {attr.option?.value}
                                                    {attr.option?.extra_price > 0 && 
                                                        ` (+${formatPrice(attr.option.extra_price)})`
                                                    }
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                )}

                                <div className="order-item-price">
                                    {formatPrice(calculateItemTotal(item))}
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
