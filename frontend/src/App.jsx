import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Account from "./pages/account"
import Home from "./pages/home"
import Menu from "./pages/menu"
import OrdersHistory from "./pages/orders_history"


function App() {
  return (
    <>
      <nav> 
        <Link to="/">Главная</Link>
        <Link to="/menu">Меню</Link>
        <Link to="/orders_history">Заказы</Link>
        <Link to="/account">Мой аккаунт</Link>
      </nav>

      <main>
        <Routes>

          <Route path="/" element={<Home />}/>
          <Route path="/menu" element={<Menu/>}/>
          <Route path="/orders_history" element={<OrdersHistory/>}/>
          <Route path="/account"element={<Account />}/>
          <Route path="*" element={<div>Страница не найдена (404)</div>}/>
        </Routes>
        </main>
    </>
  )
}

export default App
