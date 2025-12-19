import { getImageUrl, formatPrice} from '../utils/helpers';
import './ProductCard.css';

export default function ProductCard({ product, onClick }) {
    return (
        <div className="product-card" onClick={() => onClick(product)}>
            <div className="product-card-image">
                {getImageUrl(product.image_url) ? (
                    <img 
                        src={getImageUrl(product.image_url)} 
                        alt={product.name}
                        onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.parentElement.innerHTML = '<div class="product-card-placeholder">☕</div>';
                        }}
                    />
                ) : (
                    <div className="product-card-placeholder">☕</div>
                )}
            </div>
            <div className="product-card-content">
                <h3 className="product-card-name">{product.name}</h3>
                {product.description && (
                    <p className="product-card-description">{product.description}</p>
                )}
                <div className="product-card-footer">
                    <span className="product-card-price">{formatPrice(product.price)}</span>
                </div>
            </div>
        </div>
    );
}
