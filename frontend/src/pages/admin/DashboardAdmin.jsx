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


    };


    return (
        <div className="container-fluid">
            <h1>Панель администратора</h1>
            <h2>Добрый день, {user?.name}! </h2>

            <div className="row">
                <div className="col-md-8">


                </div>


            </div>
        </div>
    );
};

export default DashboardAdmin;