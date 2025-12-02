# Coffee Shop Web Site

Сайт сети кофеен  

Функции:

- Регистрация пользователей
- Просмотр кофеен и меню
- Оформление заказов
- Администратор: управление кофейнями и менеджерами


## Технологии

- Backend: Python + FastAPI  
- Frontend: React
- База данных: PostgreSQL  
- Docker

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

- coffee-postgres — имя контейнера базы
- coffee — имя пользователя
- coffee_dev — имя базы данных