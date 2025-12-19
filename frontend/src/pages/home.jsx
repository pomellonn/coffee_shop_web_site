import { Link } from 'react-router-dom';
import { useFeaturedProducts } from '../hooks/useProducts';
import { getImageUrl, formatPrice } from '../utils/helpers';
import './home.css';
import poster from '../assets/specialty Coffee-2.png';

export default function Home() {
    const { products: featuredProducts, loading, error } = useFeaturedProducts();

    return (
        <div className="home">
            {/*постер под шапкой */}
            <section className="poster-greeting">
                <img src={poster} alt="Постер кофейни" />
            </section>

            {/*Выбирают сейчас*/}
            <section className="featured-products">
                <div className="container">
                    <h2>Выбирают сейчас</h2>
                    
                    {loading && <p className="loading-text">Загрузка...</p>}
                    
                    {error && <p className="error-text">Ошибка: {error}</p>}
                    
                    {!loading && !error && featuredProducts.length > 0 && (
                        <div className="products-grid">
                            {featuredProducts.map(product => (
                                <div key={product.product_id} className="product-card">
                                    <div className="product-image">
                                        {getImageUrl(product.image_url) ? (
                                            <img 
                                                src={getImageUrl(product.image_url)} 
                                                alt={product.name}
                                                onError={(e) => {
                                                    e.target.style.display = 'none';
                                                    e.target.parentElement.innerHTML = '<div class="product-placeholder">☕</div>';
                                                }}
                                            />
                                        ) : (
                                            <div className="product-placeholder">☕</div>
                                        )}
                                    </div>
                                    <div className="product-info">
                                        <h3>{product.name}</h3>
                                        <p className="product-description">{product.description}</p>
                                        <p className="product-price">{formatPrice(product.price)}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </section>

            {/*переход к выбору кофейни */}
            <section className="cta-section">
                <div className="container">
                    <h2>Готовы сделать заказ?</h2>
                    <p>Выберите ближайшую кофейню и просмотрите наше меню</p>
                    <Link to="/menu" className="btn-secondary">
                        Выбрать кофейню
                    </Link>
                </div>
            </section>
        </div>
    );
}