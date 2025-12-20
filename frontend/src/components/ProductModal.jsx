import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getImageUrl, formatPrice } from '../utils/helpers';
import { useAuth } from '../services/AuthContext';
import { useCart } from '../services/CartContext';
import { useProductAttributes } from '../hooks/useProductAttributes';
import './ProductModal.css';

export default function ProductModal({ product, shopId, onClose }) {
    const [quantity, setQuantity] = useState(1);
    
    const { isAuthenticated } = useAuth();
    const { addToCart, setPendingItem } = useCart();
    const navigate = useNavigate();

    // Attribute name translations
    const attributeTranslations = {
        'milk': 'Молоко',
        'syrup': 'Сироп',
        'roast': 'Обжарка',
        'size': 'Размер'
    };

    const translateAttributeName = (name) => {
        const lowerName = name?.toLowerCase();
        return attributeTranslations[lowerName] || name;
    };

    // Use hook to load attributes (no initial selection)
    const { attributes, loading, error } = useProductAttributes(product?.product_id);
    
    // Store user selected options (initially empty - no pre-selection)
    const [selectedOptions, setSelectedOptions] = useState({});

    // Close modal on ESC
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

    if (!product) return null;

    const handleQuantityChange = (delta) => {
        const newQuantity = quantity + delta;
        if (newQuantity >= 1 && newQuantity <= 10) {
            setQuantity(newQuantity);
        }
    };

    const handleOptionChange = (attributeTypeId, optionId) => {
        setSelectedOptions(prev => {
            // If the same option is clicked again, deselect it
            if (prev[attributeTypeId] === optionId) {
                const newState = { ...prev };
                delete newState[attributeTypeId];
                return newState;
            }
            // Otherwise, select the new option
            return {
                ...prev,
                [attributeTypeId]: optionId
            };
        });
    };

    const calculateTotalPrice = () => {
        let total = product.price;
        
        if (attributes && Array.isArray(attributes)) {
            attributes.forEach(attr => {
                const selectedOptionId = selectedOptions[attr.attribute_type_id];
                const option = attr.options?.find(opt => opt.option_id === selectedOptionId);
                if (option) {
                    total += option.extra_price;
                }
            });
        }
        
        return total * quantity;
    };

    const handleAddToCart = () => {
        if (!isAuthenticated) {
            // Save item to add after login
            const itemToAdd = {
                product_id: product.product_id,
                quantity: quantity,
                option_ids: Object.values(selectedOptions),
                unit_price: product.price,
                shopId: shopId
            };
            setPendingItem(itemToAdd);
            
            // Show confirmation and redirect
            if (window.confirm('Вы не авторизованы. Войти?')) {
                navigate('/login', { state: { from: `/menu/${shopId}` } });
            }
            return;
        }

        // Add to cart
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

        addToCart(cartItem);
        onClose();
    };

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={onClose} aria-label="Закрыть">
                    ✕
                </button>
                
                <div className="modal-body">
                    <div className="modal-image-container">
                        {getImageUrl(product.image_url) ? (
                            <img 
                                src={getImageUrl(product.image_url)} 
                                alt={product.name}
                                className="modal-image"
                                onError={(e) => {
                                    e.target.style.display = 'none';
                                    const placeholder = document.createElement('div');
                                    placeholder.className = 'modal-image-placeholder';
                                    placeholder.textContent = '☕';
                                    e.target.parentElement.appendChild(placeholder);
                                }}
                            />
                        ) : (
                            <div className="modal-image-placeholder">☕</div>
                        )}
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

                        

                        {loading ? (
                            <div className="attributes-loading">Загрузка опций...</div>
                        ) : error ? (
                            <div className="attributes-error">{error}</div>
                        ) : Array.isArray(attributes) && attributes.length > 0 ? (
                            <div className="attributes-section">
                                <h3>Настройка напитка</h3>
                                {attributes.map((attr) => {
                                    return (
                                        <div key={attr.attribute_type_id} className="attribute-group">
                                            <label className="attribute-label">{translateAttributeName(attr.attribute_name)}:</label>
                                            <div className="attribute-options">
                                                {Array.isArray(attr.options) && attr.options.map((option) => {
                                                    return (
                                                        <button
                                                            key={option.option_id}
                                                            className={`option-btn ${
                                                                selectedOptions[attr.attribute_type_id] === option.option_id
                                                                    ? 'selected'
                                                                    : ''
                                                            }`}
                                                            onClick={() => handleOptionChange(attr.attribute_type_id, option.option_id)}
                                                        >
                                                            <span className="option-value">{option.value}</span>
                                                            {option.extra_price > 0 && (
                                                                <span className="option-price">
                                                                    +{formatPrice(option.extra_price)}
                                                                </span>
                                                            )}
                                                        </button>
                                                    );
                                                })}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <div className="attributes-info" style={{padding: '1rem', background: '#f0f0f0'}}>
                                {!loading && !error && 'У этого продукта нет дополнительных опций'}
                            </div>
                        )}

                        <div className="quantity-selector">
                            <label className="quantity-label">Количество:</label>
                            <div className="quantity-controls">
                                <button 
                                    className="quantity-btn"
                                    onClick={() => handleQuantityChange(-1)}
                                    disabled={quantity <= 1}
                                >
                                    −
                                </button>
                                <span className="quantity-value">{quantity}</span>
                                <button 
                                    className="quantity-btn"
                                    onClick={() => handleQuantityChange(1)}
                                    disabled={quantity >= 10}
                                >
                                    +
                                </button>
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
        </div>
    );
}

