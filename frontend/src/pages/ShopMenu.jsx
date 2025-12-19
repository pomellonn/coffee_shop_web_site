import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useShop } from '../hooks/useShops';
import { useShopMenu } from '../hooks/useMenu';
import ProductCard from '../components/ProductCard';
// import ProductModal from '../components/ProductModal';
import './ShopMenu.css';

export default function ShopMenu() {
    const params = useParams();
    const shopId = params.shopId ?? params.id ?? params.shop_id;
    console.debug('ShopMenu -> shopId:', shopId);

    //const [selectedProduct, setSelectedProduct] = useState(null);
    const [filter, setFilter] = useState('all');

    const { shop, loading: shopLoading, error: shopError } = useShop(shopId);
    const { menuItems, loading: menuLoading, error: menuError } = useShopMenu(shopId);

    const loading = shopLoading || menuLoading;
    const error = shopError || menuError;

    if (!shopId) return <div className="shop-not-found">Кофейня не найдена (нет id)</div>;


    // const handleAddToCart = (product) => {
    //     //TODO: Реализовать добавление в корзину
        
    // };

    //фильтрация продуктов по типу
    const filteredItems = filter === 'all' 
        ? menuItems 
        : menuItems.filter(item => {
            if (!item.product) return false;
            return item.product.product_type === filter;
        });

    //группировка типов продуктов для фильтров
    const productTypes = [
        { id: 'all', label: 'Все' },
        { id: 'coffee', label: 'Кофе'},
        { id: 'non_coffee', label: 'Напитки без кофе'},
    ];

    if (loading) {
        return (
            <div className="shop-menu-loading">
                <p>Загрузка меню...</p>
            </div>
        );
    }

    if (error || !shop) {
        return (
            <div className="shop-menu-error">
                <h2>Кофейня не найдена</h2>
                <p>{error}</p>
                <Link to="/menu" className="btn-back">← Вернуться к выбору кофейни</Link>
            </div>
        );
    }

    return (
        <div className="shop-menu">
            {/* Хедер с информацией о кофейне */}
            <div className="shop-menu-header">
                <div className="container">
                    <Link to="/menu" className="back-link">← Выбрать другую кофейню</Link>
                    <h1>☕ {shop.name}</h1>
                    <p className="shop-address">📍 {shop.address}</p>
                </div>
            </div>

            <div className="shop-menu-content">
                {/* Боковая панель с фильтрами */}
                <aside className="menu-sidebar">
                    <h3>НАПИТКИ</h3>
                    <div className="filter-buttons">
                        {productTypes.map(type => (
                            <button
                                key={type.id}
                                className={`filter-btn ${filter === type.id ? 'active' : ''}`}
                                onClick={() => setFilter(type.id)}
                            >
                                <span className="filter-icon">{type.icon}</span>
                                <span>{type.label}</span>
                            </button>
                        ))}
                    </div>
                </aside>

                {/* Сетка с продуктами */}
                <main className="menu-main">
                    {filteredItems.length === 0 ? (
                        <div className="empty-menu">
                            <p>В этой категории пока нет продуктов</p>
                        </div>
                    ) : (
                        <div className="products-grid">
                            {filteredItems.map(item => (
                                item.product && item.is_available && (
                                    <ProductCard
                                        key={item.shop_menu_id}
                                        product={item.product}
                                        // onClick={setSelectedProduct}
                                    />
                                )
                            ))}
                        </div>
                    )}
                </main>
            </div>

            {/* Модальное окно продукта
            {selectedProduct && (
                <ProductModal
                    product={selectedProduct}
                    onClose={() => setSelectedProduct(null)}
                    onAddToCart={handleAddToCart}
                />
            )} */}
        </div>
    );
}
