# Проектная работа: диплом «Кино вместе»

Выполните проект «Кино вместе»: кнопка, проверяющая список «Хочу посмотреть» у друзей пользователя и выводящая 
совпадения. 
После чего начинается сеанс совместного просмотра с чатом. Также есть общий механизм управления (пауза, перемотка) 
контентом у всех.

Экраны в клиентском приложении

![Экраны в клиентском приложении](docs/screen.jpeg)

Пример работы чата

![demo](docs/demo.gif)

## Как запустить


1) `docker-compose up -d db`
2) `psql -h localhost -p 5432 -U postgres` pwd: `postgres`
3) `create database movie_together;`
4) `\q`
5) `alembic upgrade head`
6) сгенерили таблицу с комнатами
```sql
create table movie_together_room
(
    id             uuid not null
        primary key,
    film_work_uuid uuid,
    link           varchar,
    status         varchar,
    owner_uuid     uuid not null
        unique,
    created_at     timestamp default now()
);

alter table movie_together_room
    owner to postgres;
```
7) сгенерили таблицу со связями
```sql
create table movie_together_room_user
(
    id         uuid not null
        primary key,
    user_uuid  uuid,
    room_uuid  uuid
        references movie_together_room,
    user_type  varchar,
    created_at timestamp default now(),
    constraint unique_room_user
        unique (user_uuid, room_uuid)
);

alter table movie_together_room_user
    owner to postgres;
```

## Использованы технологии

- Python 3.9
- Postgres 14
- Kafka
- Zookeeper
- FastAPI (API)
- Flask (auth)

## TODO

- Проверка лимитов на вход в комнату
- Полноценный фронтенд
- ETL процесс перекладывания данных

## Над проектом работали:
[Алексей Кучерявенко](https://github.com/frbgd)
[Олег Завитаев](https://github.com/TheZavitaev)
