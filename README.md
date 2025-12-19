# Coffee Shop Web Site

## Предметная область
Сайт сети кофеен, позволяющий пользователям оформлять заказы, просматривать меню, а администраторам и менеджерам управлять кофейнями и ассортиментом.

## Данные

### Элементы данных и ограничения

#### Пользователи (users)
- `user_id` — INTEGER, PK, уникальный идентификатор пользователя
- `email` — VARCHAR(255), уникальный, обязательный
- `password_hash` — TEXT, обязательный
- `name` — VARCHAR(50), обязательный
- `role` — ENUM('customer', 'manager', 'admin'), по умолчанию 'customer'
- `created_at` — TIMESTAMPTZ, дата создания

#### Кофейни (coffee_shops)
- `shop_id` — INTEGER, PK
- `name` — VARCHAR(128), обязательный
- `address` — VARCHAR(256), обязательный
- `manager_id` — INTEGER, UNIQUE, FK → users(user_id), при удалении менеджера — SET NULL

#### Продукты (products)
- `product_id` — INTEGER, PK
- `name` — VARCHAR(128), обязательный
- `description` — TEXT
- `image_url` — TEXT
- `volume` — INTEGER, >0
- `product_type` — ENUM('coffee', 'non_coffee', 'bakery'), обязательный
- `price` — INTEGER, ≥0

#### Меню кофейни (shop_menu)
- `shop_menu_id` — INTEGER, PK
- `shop_id` — INTEGER, FK → coffee_shops(shop_id), при удалении кофейни — CASCADE
- `product_id` — INTEGER, FK → products(product_id), при удалении продукта — RESTRICT
- `is_available` — BOOLEAN, обязательный, по умолчанию TRUE
- Уникальность комбинации (`shop_id`, `product_id`)

#### Заказы (orders)
- `order_id` — INTEGER, PK
- `user_id` — INTEGER, FK → users(user_id), RESTRICT
- `shop_id` — INTEGER, FK → coffee_shops(shop_id), RESTRICT
- `total_amount` — INTEGER, ≥0
- `created_at` — TIMESTAMPTZ

#### Позиции заказа (order_items)
- `order_item_id` — INTEGER, PK
- `order_id` — INTEGER, FK → orders(order_id), CASCADE
- `product_id` — INTEGER, FK → products(product_id), RESTRICT
- `unit_price` — INTEGER, ≥0
- `quantity` — INTEGER, ≥1

### Общие ограничения целостности
- Внешние ключи
- При удалении объектов каскадное или ограничивающее поведение по бизнес-логике

## Пользовательские роли

#### Customer
- Регистрация
- Просмотр адресов кофеен, меню -
- Оформление заказов
- Просмотр истории заказов

#### Manager
- Управление меню кофейни, менеджером которой он является
- Количество: у кофейни один менеджер

#### Admin
- Управление всеми кофейнями, менеджерами и продуктами
- Количество: 2

## UI / API
- Документация API (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Документация API также доступна в папке backend: [API](backend/README.md)

## Технологии разработки

### Язык программирования
Python

### Backend
- FastAPI
- ORM: SQLAlchemy


### Frontend
-

### СУБД
- PostgreSQL

## Тестирование
-


## Запуск проекта


```
docker-compose up --build
```

Backend доступен по адресу: http://localhost:8000

Документация API (Swagger UI): http://localhost:8000/docs


Подключение к базе данных PostgreSQL:
```
docker exec -it coffee-postgres psql -U coffee -d coffee_dev
```


# HTTPS:
Web site:
https://localhost

Swagger UI: 
https://localhost/api/docs