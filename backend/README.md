# Coffee Shop API

## Authentication

- **POST** `/api/v1/auth/token`  
  Авторизация: получение токена доступа.

---

## Users - Customer

- **POST** `/api/v1/users/register`  
  Регистрация нового пользователя.
  Создает пользователя с ролью customer и возвращает токен доступа.

  Входные данные:

  ```
  "email": "user@example.com",
  "name": "Ivan Ivanov",
  "password": "password" (min: 8 символов)
  ```

- **GET** `/api/v1/users/me`  
  Получение данных текущего пользователя.
- **PUT** `/api/v1/users/me`  
  Обновление данных текущего пользователя.

---

## Products - Public

- **GET** `/api/v1/products/`  
  Список всех продуктов.
- **GET** `/api/v1/products/{product_id}`  
  Получение продукта по ID.

---

## Shop - Public

- **GET** `/api/v1/shops/`  
  Список всех кофеен.
- **GET** `/api/v1/shops/{shop_id}`  
  Получение кофейни по ID.

---

## Shop Menu - Public

- **GET** `/api/v1/menu/{shop_id}`  
  Получение меню кофейни по ID кофейни.
- **GET** `/api/v1/menu/{shop_id}/sorted-price-asc`  
  Получение меню кофейни, отсортированного по возрастанию цены.

- **GET** `/api/v1/menu/{shop_id}/sorted-price-desc`  
  Получение меню кофейни, отсортированного по убыванию цены.

- **GET** `/api/v1/menu/{shop_id}/sorted-name-asc`  
  Получение меню кофейни, отсортированного по названию.

---

## Product Attributes - Public

- **GET** `/api/v1/products/{product_id}/attributes`  
  Получение всех доступных опций для продукта.

---

## Orders - Customer

- **POST** `/api/v1/orders/`  
  Создание нового заказа.
- **GET** `/api/v1/orders/me`  
  Получение списка заказов текущего пользователя.

---

## Users - Admin

- **GET** `/api/v1/admin/users/`  
  Список всех пользователей.
- **POST** `/api/v1/admin/users/`  
  Создание нового пользователя.
- **PUT** `/api/v1/admin/users/{user_id}`  
  Обновление данных пользователя по ID.
- **DELETE** `/api/v1/admin/users/{user_id}`  
  Удаление пользователя по ID.

---

## Products - Admin

- **POST** `/api/v1/admin/products/`  
  Создание нового продукта.

  Входные данные:

  ```
  "name": "Матча латте",
  "description": "Напиток на основе зелёного японского чая матча с молоком",
  "image_url": "https://...",
  "volume": 300,
  "product_type": "non-coffee",
  "price": 250
  ```

- **PUT** `/api/v1/admin/products/{product_id}`  
  Обновление данных о продукте по ID.
- **DELETE** `/api/v1/admin/products/{product_id}`  
  Удаление продукта по ID.

---

## Shops - Admin

- **GET** `/api/v1/admin/shops/`  
  Список всех кофеен.
- **POST** `/api/v1/admin/shops/`  
  Создание новой кофейни.

  Входные данные:

  ```
  "name": "FLTR - Nevsky",
  "address": "Санкт-Петербург, Невский проспект, 28",
  "manager_id": 1
  ```

- **GET** `/api/v1/admin/shops/{shop_id}`  
  Получение кофейни по ID.
- **PUT** `/api/v1/admin/shops/{shop_id}`  
  Обновление кофейни по ID.
- **DELETE** `/api/v1/admin/shops/{shop_id}`  
  Удаление кофейни по ID.

---

## Shop Menu - Admin

- **GET** `/api/v1/admin/menu/`  
  Список всех позиций меню.
- **POST** `/api/v1/admin/menu/`  
  Создание новой позиции меню.
- **PUT** `/api/v1/admin/menu/{menu_id}`  
  Обновление позиции меню по ID.
- **DELETE** `/api/v1/admin/menu/{menu_id}`  
  Удаление позиции меню по ID.

---

## Attribute Types - Admin

- **GET** `/api/v1/admin/attribute-types/`  
  Список всех типов атрибутов.

- **POST** `/api/v1/admin/attribute-types/`  
  Создание нового типа атрибута.

- **GET** `/api/v1/admin/attribute-types/{type_id}`  
  Получение типа атрибута по ID.

- **PUT** `/api/v1/admin/attribute-types/{type_id}`  
  Обновление типа атрибута по ID.

- **DELETE** `/api/v1/admin/attribute-types/admin/{type_id}`  
  Удаление типа атрибута по ID.

---

## Product Attributes - Admin

- **GET** `/api/v1/admin/products/{product_id}/attribute-links`  
  Список всех связей продукта с опциями.

- **POST** `/api/v1/admin/products/attribute-links`  
  Создание связи продукта с опцией.

- **DELETE** `/api/v1/admin/products/{product_id}/attribute-links/{option_id}`  
  Удаление связи продукта с опцией.

---

## Product Attribute Types Options - Admin

- **GET** `/api/v1/admin/product-attr-types-options/`  
  Список всех опций атрибутов.

- **POST** `/api/v1/admin/product-attr-types-options/`  
  Создание новой опции атрибута.
  
- **GET** `/api/v1/admin/product-attr-types-options/{option_id}`  
  Получение опции атрибута по ID.

- **PUT** `/api/v1/admin/product-attr-types-options/{option_id}`  
  Обновление опции атрибута по ID.

- **DELETE** `/api/v1/admin/product-attr-types-options/{option_id}`  
  Удаление опции атрибута по ID.

## Analytics - Admin

- **GET** `/api/v1/admin/analytics/shops/one`  
  Аналитика по одной кофейне.
- **GET** `/api/v1/admin/analytics/shops/all`  
  Аналитика по всем кофейням.
- **GET** `/api/v1/admin/analytics/clients/top`  
  Топ клиентов по заказам.
- **GET** `/api/v1/admin/analytics/clients/stats`  
  Статистика по клиентам.

---

## Orders - Admin

- **GET** `/api/v1/admin/orders/`  
  Список всех заказов.

---

## Shops - Manager

- **GET** `/api/v1/manager/shops/info`  
  Получение информации о кофейне менеджера.

---

## Shop Menu - Manager

- **GET** `/api/v1/manager/menu/`  
  Меню кофейни менеджера.
- **POST** `/api/v1/manager/menu/`  
  Добавление продукта в меню.
- **PUT** `/api/v1/manager/menu/{menu_id}`  
  Обновление позиции меню.
- **DELETE** `/api/v1/manager/menu/{menu_id}`  
  Удаление позиции меню.

---

## Analytics - Manager

- **GET** `/api/v1/manager/analytics/`  
  Аналитика по кофейне менеджера.

---

## Orders - Manager

- **GET** `/api/v1/manager/orders/`  
  Получение всех заказов для кофейни менеджера.

- **GET** `/api/v1/manager/orders/today`  
  Получение заказов для кофейни менеджера за сегодня.

- **GET** `/api/v1/manager/orders/orders-count`  
  Получение количества заказов для кофейни менеджера за день.

---

### Аналитика по одной кофейне за выбранный период времени

- **Заказы по дням**  
  Количество заказов за каждый день.
- **Заказы по месяцам**  
  Количество заказов, выручка и средний чек по месяцам для кофейни.
- **Продукция**  
  Топ-продуктов по количеству продаж и выручке для кофейни менеджера.
- **Продажи по времени суток**  
  Количество заказов по временным интервалам (утро, день, вечер).

### Аналитика по всем кофейням за выбранный период времени

- **Заказы по дням**  
  Количество заказов за каждый день.
- **Заказы по месяцам**  
  Количество заказов, выручка и средний чек.
- **Рейтинг продуктов**  
  Топ-продуктов по количеству продаж и выручке.
- **Продажи по времени суток**  
  Количество заказов по временным интервалам (утро, день, вечер) для всех кофеен.
- **Средний чек, количество заказов и общая выручка по каждой кофейне.**  
  

### Клиентская аналитика за выбранный период времени

- **Топ клиентов**  
  Топ-20 клиентов по количеству покупок, потраченным деньгам и посещённым кофейням.
- **Статистика клиентов**  
  Соотношение новых и постоянных клиентов.
