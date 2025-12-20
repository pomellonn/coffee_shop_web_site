import { Link } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import './Header.css';
import logo from '../assets/logo.svg';

export default function Header() {
  const { isAuthenticated } = useAuth();
  
  let menuLink = '/menu';
  try {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      const cart = JSON.parse(savedCart);
      if (cart.length > 0 && cart[0].shopId) {
        menuLink = `/menu/${cart[0].shopId}`;
      }
    }
  } catch (error) {
    //if localStorage fails use default menu link
    console.error('Error reading cart from localStorage:', error);
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
          <Link to={menuLink}>Меню</Link>
          {isAuthenticated ? (
            <>
              <Link to="/account">Личный кабинет</Link>
              <Link to="/cart" className="cart-link">Корзина</Link>
            </>
          ) : (
            <Link to="/login">Войти</Link>
          )}
        </nav>
      </div>
    </header>
  );
}
