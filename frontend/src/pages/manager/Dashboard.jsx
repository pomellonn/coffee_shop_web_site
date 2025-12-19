import { useEffect, useState } from "react";
import { getOrdersCount, getShopInfo, getTodayOrders } from "../../services/managerService";
import { getCurrentUser } from "../../services/authService";

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [todayOrdersCount, setTodayOrdersCount] = useState(0);
  const [shopInfo, setShopInfo] = useState(null);
  const [orders, setOrders] = useState([]);

  // Пагинация
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const userData = await getCurrentUser();
    setUser(userData);

    const ordersCount = await getOrdersCount();
    setTodayOrdersCount(ordersCount);

    const info = await getShopInfo();
    setShopInfo(info);

    const todayOrders = await getTodayOrders();
    setOrders(todayOrders);
  };

  // Пагинация
  const indexOfLastOrder = currentPage * pageSize;
  const indexOfFirstOrder = indexOfLastOrder - pageSize;
  const currentOrders = orders.slice(indexOfFirstOrder, indexOfLastOrder);
  const totalPages = Math.ceil(orders.length / pageSize);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="min-h-screen">
      <div className="px-10">
        {/* Заголовок */}
        <h1 className="text-3xl font-light text-gray-900 mb-2">Панель менеджера</h1>
        <p className="text-gray-600 mb-12">Добрый день, {user?.name}!</p>

        {/* Информационные карточки */}
        <div className="grid grid-cols-3 gap-8 mb-20">
          <div className="col-span-2 border border-gray-200 p-6">
            <h2 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
              Ваша кофейня
            </h2>
            {shopInfo ? (
              <div className="space-y-2">
                <p className="text-gray-900">
                  <span className="text-gray-500">Название:</span> {shopInfo.name}
                </p>
                <p className="text-gray-900">
                  <span className="text-gray-500">Адрес:</span> {shopInfo.address}
                </p>
              </div>
            ) : (
              <p className="text-gray-500">Вы не управляете ни одной кофейней</p>
            )}
          </div>

          <div className="border border-gray-200 p-6">
            <h2 className="text-sm text-gray-500 uppercase tracking-wide mb-4">
              Заказы за сегодня
            </h2>
            <p className="text-4xl font-light text-gray-900">{todayOrdersCount}</p>
          </div>
        </div>

        {/* Заказы */}
        <div className="mb-20">
          <h2 className="text-2xl font-light text-gray-900 mb-8">
            Сегодняшние заказы
          </h2>

          {/* Заголовки таблицы */}
          <div className="flex items-center py-3 border-b border-gray-300 mb-1">
            <span className="text-xs text-gray-500 uppercase tracking-wide w-24">
              Order ID
            </span>
            <span className="text-xs text-gray-500 uppercase tracking-wide w-48">
              Дата и время
            </span>
            <span className="text-xs text-gray-500 uppercase tracking-wide w-32">
              Пользователь
            </span>
            <span className="text-xs text-gray-500 uppercase tracking-wide w-32 text-center">
              Позиций
            </span>
            <span className="text-xs text-gray-500 uppercase tracking-wide w-32 text-right">
              Сумма
            </span>
          </div>

          {/* Список заказов */}
          <div className="space-y-1">
            {currentOrders.length > 0 ? (
              currentOrders.map(order => (
                <div
                  key={order.order_id}
                  className="flex items-center py-4 border-b border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <span className="text-gray-900 text-sm w-24">
                    {order.order_id}
                  </span>
                  <span className="text-gray-900 text-sm w-48">
                    {new Date(order.created_at).toLocaleString('ru-RU', {
                      day: '2-digit',
                      month: '2-digit',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                  <span className="text-gray-900 text-sm w-32">
                    {order.user_id}
                  </span>
                  <span className="text-gray-900 text-sm w-32 text-center">
                    {order.items.length}
                  </span>
                  <span className="text-gray-900 text-sm w-32 text-right">
                    {order.total_amount} руб.
                  </span>
                </div>
              ))
            ) : (
              <div className="py-16 text-center text-gray-400 text-sm">
                Заказов нет
              </div>
            )}
          </div>
        </div>

        {/* Пагинация */}
        {totalPages > 1 && (
          <div className="flex justify-center mb-20 gap-2">
            {Array.from({ length: totalPages }, (_, i) => (
              <button
                key={i + 1}
                onClick={() => handlePageChange(i + 1)}
                className={`px-3 py-1 text-sm transition-colors ${
                  currentPage === i + 1
                    ? "text-gray-900 font-medium border-b-2 border-gray-900"
                    : "text-gray-400 hover:text-gray-600"
                }`}
              >
                {i + 1}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;