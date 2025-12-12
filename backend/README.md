# API
Базовый URL API: /api/v1

## Аутентификация


```POST /auth/token```
Получение JWT токена.

Входные данные: 
- email
- password


```POST /users/register```
Регистрация нового пользователя.

Создает нового пользователя с ролью customer и возвращает токен доступа.

Входные данные:
  ``` 
  "email": "user@example.com",
  "name": "Ivan Ivanov",
  "password": "password" (min: 8 символов)
  ```


## Пользователи (Users)
Доступно для пользователей, вошедших в систему

```GET /users/me```
Получение информации о текущем пользователе.

```PUT /users/me```
Обновление информации (email, name) о текущем пользователе.

### Администрирование (Admin)
Требуемая роль: admin

```GET /users/```
Получение списка всех пользователей.

```POST /users/admin/create```
Создание нового пользователя с ролью:  customer/manager/admin.


```PUT /users/{user_id}```
Обновление данных пользователя по ID.

```DELETE /users/{user_id}```
Удаление пользователя по ID.


## Кофейни, входящие в сеть (coffee_shops)

### Администратор

```GET /api/v1/shops/admin```
Получение списка всех кофеен, по связи с таблицей Users выводит имя и email менеджера.


```GET /api/v1/shops/admin/{shop_id}```
Получение конкретной кофейни по ID, по связи с таблицей Users выводит имя и email менеджера.

```POST /api/v1/shops/```
Создание новой кофейни.

Входные данные:
  ``` 
"name": "gotcha - Nevsky",
  "address": "Санкт-Петербург, Невский проспект, 28",
  "manager_id": 1
  ```

```PUT /api/v1/shops/{shop_id}```
Обновление данных кофейни.


```DELETE /api/v1/shops/{shop_id}```
Удаление кофейни по ID.



### Customer

```GET /api/v1/shops/```
Получение списка всех кофеен.

```GET /api/v1/shops/{shop_id}```
Получение конкретной кофейни по ID.

## Продукция кофейни (products)

```GET /products/ ```
Получить список всех продуктов.

Доступ: все пользователи (customer, manager, admin)

```POST /products/ ```
Создание нового продукта.
Доступ: manager, admin
Входные данные: 
```
"name": "Матча латте",
"description": "Напиток на основе зелёного японского чая матча с молоком",
"image_url": "https://...",
"volume": 300,
"product_type": "non-coffee",
"price": 250
```

```GET /products/{product_id}```
Получение данных о продукте по его id.

Доступ: все пользователи (customer, manager, admin)

```PUT /products/{product_id}```
Обновление данных о продукте по id.

Доступ: manager, admin

```DELETE /products/{product_id}```
Удаление продукта по id.

Доступ: manager, admin