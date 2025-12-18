import { useEffect, useState } from "react";
import Menu from "../menu";
// import Analytics from "./Analytics";
import { getOrdersCount, getShopInfo } from "../../services/managerService";
import { getCurrentUser } from "../../services/authService";
const DashboardAdmin = () => {
    const [menuItems, setMenuItems] = useState([]);
    const [analytics, setAnalytics] = useState(null);
    const [user, setUser] = useState(null);
    const [todayOrders, setTodayOrders] = useState(0);
    const [shopInfo, setShopInfo] = useState(null);
    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        const user = await getCurrentUser();
        setUser(user);
        const ordersCount = await getOrdersCount();
        setTodayOrders(ordersCount);
        const info = await getShopInfo();
        setShopInfo(info);
    };


    return (
        <div className="container-fluid">
            <h1>Панель администратора</h1>
            <h2>Добрый день, {user?.name}! </h2>

            <div className="row">
                <div className="col-md-8">
                    <h5>Ваша кофейня</h5>
                    {shopInfo ? (
                        <>
                            <p>Название: {shopInfo?.name}</p>
                            <p>Адрес: {shopInfo?.address}</p>
                        </>
                    ) : (<p> Вы не управляете ни одной кофейней сети
                    </p>
                    )}
                </div>
                <div className="card p-3">
                    <h5>Заказы за сегодня</h5>
                    <p style={{ fontSize: "24px", fontWeight: "bold" }}>{todayOrders}</p>
                </div>

            </div>
        </div>
    );
};

export default DashboardAdmin;