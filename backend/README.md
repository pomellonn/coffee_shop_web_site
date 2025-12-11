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

```GET /shops/```
Получить список всех кофеен.

```POST /shops/```
Создать новую кофейню.

```GET /shops/{shop_id}```
Получить кофейню по id.

```PUT /shops/{shop_id}```
Обновить данные о кофейне по id.

```DELETE /shops/{shop_id}```
Удалить кофейню по id.

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