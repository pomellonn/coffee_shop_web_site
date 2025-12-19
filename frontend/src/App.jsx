import React from 'react';
import { Routes, Route, Outlet, useLocation } from 'react-router-dom'
import Account from "./pages/customerAccount"
import Home from "./pages/home"
import MenuShopSelector from "./pages/MenuShopSelector"
import ShopMenu from "./pages/ShopMenu"
import OrdersHistory from "./pages/orders_history"
import Login from "./pages/login"
import Register from "./pages/register"
import ProtectedRoute from "./services/PrRoute.jsx"
import { AuthProvider } from './services/AuthContext.jsx';
import Dashboard from './pages/manager/Dashboard.jsx';
import LayoutManager from "./components/admin/LayotManager.jsx";
import LayoutAdmin from "./components/admin/LayotAdmin.jsx";
import AnalyticsManager from "./pages/manager/AnalyticsManager.jsx";
import ManagerMenu from './pages/manager/MenuManager.jsx';
import AnalyticsAllShopsAdmin from './pages/admin/AnalyticsAllShopsAdmin.jsx'
import CoffeeShopsAdmin from './pages/admin/CoffeeShopsAdmin.jsx';
import DashboardAdmin from './pages/admin/DashboardAdmin.jsx';
import ProductsAdmin from './pages/admin/ProductsAdmin.jsx';
import UsersAdmin from './pages/admin/UsersAdmin.jsx';
import Header from './components/Header.jsx';
import ClientsAnalytics from './pages/admin/ClientsAnalytics.jsx';
import AnalyticsOneShopAdmin from './pages/admin/AnalyticsOneShopAdmin.jsx';

function App() {
  const location = useLocation();
  const hideHeader = ['/admin', '/manager'].some(p => location.pathname.startsWith(p));
  return (
    <>
      <main>
        <AuthProvider>
          {/* <Header /> */}
          {!hideHeader && <Header />}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/menu" element={<MenuShopSelector />} />
            <Route path="/menu/:shopId" element={<ShopMenu />} />
            <Route path="/account" element={<Account />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="*" element={<div>Страница не найдена (404)</div>} />



            <Route element={<LayoutManager><Outlet /></LayoutManager>}>
              <Route element={<ProtectedRoute roles={["manager"]} />}>
                <Route path="/manager" element={<Dashboard />} />
                <Route path="/manager/menu" element={<ManagerMenu />} />
                <Route path="/manager/analytics" element={<AnalyticsManager />} />

              </Route>
            </Route>

            <Route element={<LayoutAdmin><Outlet /></LayoutAdmin>}>
              <Route element={<ProtectedRoute roles={["admin"]} />}>
                <Route path="/admin" element={<DashboardAdmin />} />
                <Route path="/admin/analyticsAllShops" element={<AnalyticsAllShopsAdmin />} />
                <Route path="/admin/users" element={<UsersAdmin />} />
                <Route path="/admin/products" element={<ProductsAdmin />} />
                <Route path="/admin/shops" element={<CoffeeShopsAdmin />} />
                <Route path="/admin/analyticsClients" element={< ClientsAnalytics/>} />
                <Route path="/admin/analyticsOneShop" element={<AnalyticsOneShopAdmin />} />
              </Route>
            </Route>





          </Routes>
        </AuthProvider>
      </main>
    </>
  )
}

export default App