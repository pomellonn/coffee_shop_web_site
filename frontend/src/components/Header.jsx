import { Link } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import { useCart } from '../services/CartContext';
import './Header.css';
import logo from '../assets/logo.svg';

export default function Header() {
  const { isAuthenticated } = useAuth();
  // Only use cart hook if we're in a customer route
  let cartCount = 0;
  try {
    const cart = useCart();
    cartCount = cart?.getCartCount() || 0;
  } catch {
    // Cart context not available in this route
  }
  
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-logo">
          <Link to="/">
            <img src={logo} alt="кофейня FLTR" className="logo-image" />
          </Link>
        </div>
        <nav className="header-nav">
          <Link to="/menu">Меню</Link>
          <Link to="/shops">Адреса</Link>
          {isAuthenticated ? (
            <>
              <Link to="/account">Личный кабинет</Link>
              <Link to="/cart" className="cart-link">
                🛒 Корзина
                {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
              </Link>
            </>
          ) : (
            <Link to="/login">Войти</Link>
          )}
        </nav>
      </div>
    </header>
  );
}
