import { Outlet, Link } from 'react-router-dom';

const LayoutAdmin = () => {
  return (
    <div className="min-h-screen">
      <aside className="fixed left-0 top-0 w-64 h-screen bg-slate-800 text-white p-5 overflow-y-auto">
        <h2 className="text-xl font-semibold text-center mb-8">Администратор</h2>
        <nav>
          <ul className="space-y-3">
            <li >
              <Link to="/admin" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Главная</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/users" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Клиенты</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/products" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Продукция кофейни</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/shops" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Кофейни сети</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/analyticsOneShop" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Аналитика по одной кофейне</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/analyticsAllShops" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Аналитика всех кофеен</span>
              </Link>
            </li>
            <li>
              <Link to="/admin/analyticsClients" className="flex items-center gap-3 px-3 py-2 rounded hover:bg-slate-700">
                <span>Анализ клиентов</span>
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

export default LayoutAdmin;
