import { useEffect, useState } from "react";
import Menu from "../menu";
// import Analytics from "./Analytics";
import { getShopMenu } from "../../services/managerService";

const Dashboard = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const menu = await getShopMenu();
    setMenuItems(menu);

    // const analyticsData = await getManagerAnalytics();
    // setAnalytics(analyticsData);
  };

  return (
    <div className="container-fluid">
      <h1>Менеджерская панель</h1>
      
      <div className="row">
        <div className="col-md-8">
          {/* <Menu menuItems={menuItems} refresh={fetchData} /> */}
        </div>
        {/* <div className="col-md-4">
          {analytics && <Analytics data={analytics} />}
        </div> */}
      </div>
    </div>
  );
};

export default Dashboard;