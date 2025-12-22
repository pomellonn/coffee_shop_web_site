import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { formatPrice, translateAttributeName } from '../utils/helpers';
import { useAuth } from '../services/AuthContext';
import { useCart } from '../services/CartContext';
import { useProductAttributes } from '../hooks/useProductAttributes';
import { useModal } from '../hooks/useModal';
import { calculateProductTotal } from '../utils/priceCalculators';
import ProductImage from './ProductImage';
import './ProductModal.css';

export default function ProductModal({ product, shopId, onClose }) {
    const [quantity, setQuantity] = useState(1);
    
    const { isAuthenticated } = useAuth();
    const { addToCart, setPendingItem } = useCart();
    const navigate = useNavigate();

    const { attributes, loading, error } = useProductAttributes(product?.product_id);
    
    const [selectedOptions, setSelectedOptions] = useState({});
    useModal(onClose);

    if (!product) return null;

    const handleQuantityChange = (delta) => {
        const newQuantity = quantity + delta;
        if (newQuantity >= 1 && newQuantity <= 10) {
            setQuantity(newQuantity);
        }
    };

    const handleOptionChange = (attributeTypeId, optionId) => {
        setSelectedOptions(prev => {
            if (prev[attributeTypeId] === optionId) {
                const newState = { ...prev };
                delete newState[attributeTypeId];
                return newState;
            }

            return {
                ...prev,
                [attributeTypeId]: optionId
            };
        });
    };

    const calculateTotalPrice = () => {
        return calculateProductTotal(product.price, attributes, selectedOptions, quantity);
    };

    const handleAddToCart = () => {
        const selectedOptionsDetails = [];
        if (attributes && Array.isArray(attributes)) {
            attributes.forEach(attr => {
                const selectedOptionId = selectedOptions[attr.attribute_type_id];
                const option = attr.options?.find(opt => opt.option_id === selectedOptionId);
                if (option) {
                    selectedOptionsDetails.push({
                        option_id: option.option_id,
                        attribute_type: attr.attribute_name,
                        value: option.value,
                        extra_price: option.extra_price
                    });
                }
            });
        }

        const cartItem = {
            product_id: product.product_id,
            product_name: product.name,
            quantity: quantity,
            option_ids: Object.values(selectedOptions),
            unit_price: product.price,
            selected_options: selectedOptionsDetails,
            shopId: shopId
        };

        if (!isAuthenticated) {
            setPendingItem(cartItem);
            
            if (window.confirm('Вы не авторизованы. Войти?')) {
                navigate('/login', { state: { from: `/menu/${shopId}` } });
            }
            return;
        }

        addToCart(cartItem);
        onClose();
    };


    let attributesContent;
    if (loading) {
        attributesContent = <div className="attributes-loading">Загрузка опций...</div>;
    } else if (error) {
        attributesContent = <div className="attributes-error">{error}</div>;
    } else if (Array.isArray(attributes) && attributes.length > 0) {
        attributesContent = (
            <div className="attributes-section">
                <h3>Настройка напитка</h3>
                {attributes.map((attr) => (
                    <div key={attr.attribute_type_id} className="attribute-group">
                        <label className="attribute-label">{translateAttributeName(attr.attribute_name)}:</label>
                        <div className="attribute-options">
                            {Array.isArray(attr.options) && attr.options.map((option) => (
                                <button
                                    key={option.option_id}
                                    className={`option-btn ${selectedOptions[attr.attribute_type_id] === option.option_id ? 'selected' : ''}`}
                                    onClick={() => handleOptionChange(attr.attribute_type_id, option.option_id)}
                                >
                                    <span className="option-value">{option.value}</span>
                                    {option.extra_price > 0 && (
                                        <span className="option-price">+{formatPrice(option.extra_price)}</span>
                                    )}
                                </button>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        );
    } else {
        attributesContent = (
            <div className="attributes-info" style={{ padding: '1rem', background: '#f0f0f0' }}>
                {!loading && !error && 'У этого продукта нет дополнительных опций'}
            </div>
        );
    }

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={onClose} aria-label="Закрыть">✕</button>

                <div className="modal-image-container">
                    <ProductImage
                        imageUrl={product.image_url}
                        productName={product.name}
                        className="modal-image"
                        placeholderClassName="modal-image-placeholder"
                    />
                </div>

                <div className="modal-info">
                    <h2>{product.name}</h2>

                    {product.description && (
                        <p className="modal-description">{product.description}</p>
                    )}

                    <div className="modal-price">
                        <span className="price-label">Базовая цена:</span>
                        <span className="price-value">{formatPrice(product.price)}</span>
                    </div>

                    {attributesContent}

                    <div className="quantity-selector">
                        <label className="quantity-label">Количество:</label>
                        <div className="quantity-controls">
                            <button className="quantity-btn" onClick={() => handleQuantityChange(-1)} disabled={quantity <= 1}>−</button>
                            <span className="quantity-value">{quantity}</span>
                            <button className="quantity-btn" onClick={() => handleQuantityChange(1)} disabled={quantity >= 10}>+</button>
                        </div>
                    </div>

                    <div className="modal-total">
                        <span className="total-label">Итого:</span>
                        <span className="total-value">{formatPrice(calculateTotalPrice())}</span>
                    </div>

                        <button 
                            className="add-to-cart-btn"
                            onClick={handleAddToCart}
                            disabled={loading}
                        >
                            {isAuthenticated ? 'Добавить в корзину' : 'Войти и добавить'}
                        </button>
                    </div>
                </div>
            </div>
    );
}

