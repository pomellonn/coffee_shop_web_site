import { Link } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import './Header.css';
import logo from '../assets/logo.svg';

export default function Header() {
  const {isAuthenticated } = useAuth();
  
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
              <Link to="/cart"> Корзина</Link>
            </>
          ) : (
            <Link to="/login">Войти</Link>
          )}
        </nav>
      </div>
    </header>
  );
}
