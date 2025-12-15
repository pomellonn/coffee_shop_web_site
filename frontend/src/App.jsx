import React from 'react';
import { Routes, Route, Link } from 'react-router-dom'
import Account from "./pages/customerAccount"
import Home from "./pages/home"
import Menu from "./pages/menu"
import OrdersHistory from "./pages/orders_history"
import Login from "./pages/login"
import Register from "./pages/register"



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
        <Routes>

          <Route path="/" element={<Home />}/>
          <Route path="/menu" element={<Menu/>}/>
          <Route path="/orders_history" element={<OrdersHistory/>}/>
          <Route path="/customerAccount"element={<Account />}/>
          <Route path="/login" element={<Login />}/>
          <Route path="/register" element={<Register />}/>
          <Route path="*" element={<div>Страница не найдена (404)</div>}/>
  
        </Routes>
        </main>
    </>
  )
}

export default App
