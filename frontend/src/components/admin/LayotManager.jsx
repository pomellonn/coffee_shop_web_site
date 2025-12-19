import { Outlet, Link } from 'react-router-dom';
const LayoutManager = () => {
  return (
    <div className="min-h-screen">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 w-64 h-screen bg-slate-800 text-white p-5 overflow-y-auto">
        <h2 className="text-xl font-semibold text-center mb-8">Менеджер</h2>
        <nav>
          <ul className="space-y-3">
            <li>
              <Link to="/manager" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Главная</span>
              </Link>
            </li>
            <li>
              <Link to="/manager/menu" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Меню кофейни</span>
              </Link>
            </li>
            <li>
              <Link to="/manager/analytics" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Аналитика</span>
              </Link>
            </li>
            <li>
              <Link to="/login" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Выход</span>
              </Link>
            </li>
          </ul>
        </nav>
      </aside>

      <main className="ml-64 bg-slate-50 min-h-screen p-6">
        <Outlet />
      </main>
    </div>
  );
};

export default LayoutManager;
