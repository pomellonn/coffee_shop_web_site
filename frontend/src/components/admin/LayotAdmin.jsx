import { Outlet } from 'react-router-dom';
import './styles.css'
const LayoutAdmin = () => {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <h2 className="logo">Администратор</h2>
        <nav className="menu">
          <ul>
            <li>
              <a href="/admin">

                <span>Главная</span>
              </a>
            </li>
            <li>
              <a href="/admin/users">
                <span>Клиенты</span>
              </a>
            </li>
            <li>
              <a href="/admin/products">
                <span>Продукция кофейни</span>
              </a>
            </li>
            <li>
              <a href="/admin/shops">
                <span>Кофейни сети</span>
              </a>
            </li>
            <li>
              <a href="/admin">
                <span>Аналитика по одной кофейне</span>
              </a>
            </li>
            <li>
              <a href="/admin/analyticsAllShops">

                <span>Аналитика всех кофеен</span>
              </a>
            </li>
            <li>
              <a href="/admin">

                <span>Анализ клиентов</span>
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
};

export default LayoutAdmin;
