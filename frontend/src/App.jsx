import React from 'react';
import { Routes, Route, Link, Outlet } from 'react-router-dom'
import Account from "./pages/customerAccount"
import Home from "./pages/home"
import Menu from "./pages/menu"
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
function App() {
  return (
    <>
      <nav>
        <Link to="/home">Главная</Link>
        <Link to="/menu">Меню</Link>
        <Link to="/orders_history">Заказы</Link>
        <Link to="/customerAccount">Мой аккаунт</Link>
        <Link to="/login">Войти в аккаунт</Link>
        <Link to="/register">Зарегистрироваться</Link>

      </nav>

      <main>

        <AuthProvider>
          <Routes>

            <Route path="/" element={<Home />} />
            {/* <Route path="/menu" element={<Menu />} /> */}
            <Route path="/orders_history" element={<OrdersHistory />} />
            <Route path="/customerAccount" element={<Account />} />
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
            
              </Route>
            </Route>



          </Routes>
        </AuthProvider>
      </main>
    </>
  )
}

export default App
