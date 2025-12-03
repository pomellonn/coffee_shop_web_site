# API
## Пользователи (users)
```POST /auth/register``` 
Регистрация пользователя.

```POST /auth/token``` 
Получение JWT токена (логин).

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

```POST /products/ ```
Создать новый продукт.

```GET /products/{product_id}```
Получить данные о продукте по его id.

```PUT /products/{product_id}```
Обновить данные о продукте по id.

```DELETE /products/{product_id}```
Удалить продукт из базы данных по id.