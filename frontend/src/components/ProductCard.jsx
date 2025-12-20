import { formatPrice } from '../utils/helpers';
import ProductImage from './ProductImage';
import './ProductCard.css';

export default function ProductCard({ product, onClick }) {
    return (
        <div className="product-card" onClick={() => onClick(product)}>
            <div className="product-card-image">
                <ProductImage
                    imageUrl={product.image_url}
                    productName={product.name}
                    placeholderClassName="product-card-placeholder"
                />
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
