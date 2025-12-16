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
import Layout from "./components/admin/Layot";
import AnalyticsManager from "./pages/manager/AnalyticsManager.jsx";
import ManagerMenu from './pages/manager/MenuManager.jsx';
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

         

            <Route element={<Layout><Outlet /></Layout>}>
              <Route element={<ProtectedRoute roles={["manager"]} />}>
                <Route path="/manager" element={<Dashboard />} />
                <Route path="/manager/menu" element={<ManagerMenu />} />
                <Route path="/manager/analytics" element={<AnalyticsManager />} />
               
              </Route>
            </Route>



            {/* admin */}
            <Route element={<ProtectedRoute roles={['admin']} />}>
              <Route path="/admin_smth" element={<Menu />} />
              <Route path="/admin" element={<div>Управление пользователями (Admin Only)</div>} />
            </Route>

          </Routes>
        </AuthProvider>
      </main>
    </>
  )
}

export default App
