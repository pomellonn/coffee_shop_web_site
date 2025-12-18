import { useEffect, useState } from "react";
import { getOrdersCount, getShopInfo, getTodayOrders } from "../../services/managerService";
import { getCurrentUser } from "../../services/authService";

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const [todayOrdersCount, setTodayOrdersCount] = useState(0);
    const [shopInfo, setShopInfo] = useState(null);
    const [orders, setOrders] = useState([]);

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

    return (
        <div className="container-fluid">
            <h1>Панель менеджера</h1>
            <h2>Добрый день, {user?.name}!</h2>

            <div className="row mb-4">
                <div className="col-md-8">
                    <h5>Ваша кофейня</h5>
                    {shopInfo ? (
                        <>
                            <p>Название: {shopInfo.name}</p>
                            <p>Адрес: {shopInfo.address}</p>
                        </>
                    ) : (
                        <p>Вы не управляете ни одной кофейней сети</p>
                    )}
                </div>
                <div className="col-md-4">
                    <div className="card p-3">
                        <h5>Заказы за сегодня</h5>
                        <p style={{ fontSize: "24px", fontWeight: "bold" }}>{todayOrdersCount}</p>
                    </div>
                </div>
            </div>

            {/* Таблица заказов */}
            <h5>Сегодняшние заказы</h5>
            <table className="table table-bordered">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Дата и время</th>
                        <th>Пользователь</th>
                        <th>Количество позиций</th>
                        <th>Сумма</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.length > 0 ? (
                        orders.map(order => (
                            <tr key={order.order_id}>
                                <td>{order.order_id}</td>
                                <td>{new Date(order.created_at).toLocaleString()}</td>
                                <td>{order.user_id}</td>
                                <td>{order.items.length}</td>
                                <td>{order.total_amount} руб.</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="5" style={{ textAlign: "center" }}>Заказов нет</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default Dashboard;