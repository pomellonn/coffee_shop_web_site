import { getImageUrl } from '../utils/helpers';

/**
 * Reusable component for displaying product images with fallback
 * @param {string} imageUrl - Image URL
 * @param {string} productName - Product name for alt text
 * @param {string} className - CSS class for image container
 * @param {string} placeholderClassName - CSS class for placeholder
 */
export default function ProductImage({ imageUrl, productName, className = '', placeholderClassName = '' }) {
    const url = getImageUrl(imageUrl);

    const handleImageError = (e) => {
        e.target.style.display = 'none';
        const placeholder = document.createElement('div');
        placeholder.className = placeholderClassName || 'product-placeholder';
        placeholder.innerHTML = '<span class="material-symbols-outlined">coffee_maker</span>';
        e.target.parentElement.appendChild(placeholder);
    };

    if (!url) {
        return (
            <div className={placeholderClassName || 'product-placeholder'}>
                <span className="material-symbols-outlined">coffee_maker</span>
            </div>
        );
    }

    return (
        <img 
            src={url} 
            alt={productName}
            className={className}
            onError={handleImageError}
        />
    );
}
