1) `cd movie_together`
2) `docker-compose up -d db`
3) `pip install -r movie_together/app/requirements.txt`
4) `psql -h localhost -p 5432 -U postgres` pwd: `postgres`
5) `create database movie_together;`
6) `\q`
7) `alembic upgrade head`

Если я где-то накосячил:

1) создали БД
```sql
create database movie_together;
```

2) сгенерили таблицу с комнатами
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

3) сгенерили таблицу со связями
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

payload
```json
{
    "username": "TheZavitaev",
    "first_name": "Oleg",
    "last_name": "Zavitaev",
    "email": "o.zavitaev@yandex.ru",
    "sub": "6ad3a14e-2ffd-4e3a-9013-b981a202b159"
}
```

jwt
`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlRoZVphdml0YWV2IiwiZmlyc3RfbmFtZSI6Ik9sZWciLCJsYXN0X25hbWUiOiJaYXZpdGFldiIsImVtYWlsIjoiby56YXZpdGFldkB5YW5kZXgucnUiLCJzdWIiOiI2YWQzYTE0ZS0yZmZkLTRlM2EtOTAxMy1iOTgxYTIwMmIxNTkifQ.E34XClyBGQV5414J-CUYGQYX-7ILylnxK6Ppr1QdHM0`


