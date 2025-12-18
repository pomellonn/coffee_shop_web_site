import { Outlet } from 'react-router-dom';
import './styles.css'
const LayoutManager = () => {
  return (
    <div className="app-layot">
      <aside className="sidebar">
        <h2 className="logo">Менеджер</h2>
        <nav className="menu">
          <ul>
            <li>
              <a href="/manager">

                <span>Главная</span>
              </a>
            </li>
            <li>
              <a href="/manager/menu">

                <span>Меню кофейни</span>
              </a>
            </li>
            <li>
              <a href="/manager/analytics">

                <span>Аналитика</span>
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

export default LayoutManager;
