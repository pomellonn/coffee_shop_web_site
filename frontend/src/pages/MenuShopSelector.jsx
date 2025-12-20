import { Link } from 'react-router-dom';
import { useShops } from '../hooks/useShops';
import './MenuShopSelector.css';

export default function MenuShopSelector() {
    const { shops, loading: shopsLoading, error: shopsError } = useShops();
    // if (shopsLoading) return <div className="menu-selector-loading">Загрузка...</div>;
    if (shopsError) return <div className="menu-selector-error">Ошибка: {String(shopsError)}</div>;

    return (
        <div className="menu-shop-selector">
            <section className="shops-section">
                <div className="container">
                    <h2> Выберите ближайшую кофейню</h2>
                    <p className="subtitle">Нажмите на кофейню, чтобы увидеть меню</p>
                    
                    <div className="shops-grid">
                        {shopsLoading ? (
                            <p>Загрузка...</p>
                        ) : shops.length === 0 ? (
                            <p>Кофейни не найдены</p>
                        ) : (
                            shops.map(shop => {
                                const id = shop.shop_id 
                                return (
                                <Link key={id} to={`/menu/${encodeURIComponent(id)}`} className="shop-card">
                                    <div className="shop-icon">
                                        <span className="material-symbols-outlined">coffee_maker</span>
                                    </div>
                                    <div className="shop-info">
                                    <h3>{shop.name}</h3>
                                    {shop.address && (
                                        <p className="shop-address">
                                            <span className="material-symbols-outlined">location_on</span>
                                            {shop.address}
                                        </p>
                                    )}
                                    </div>
                                </Link>
                                );
                            })
                        )}
                    </div>
                </div>
            </section>
        </div>
    );
}
