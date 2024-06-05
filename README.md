# FastAPI-Redis-ETL

# User info service

Приложение для записи, получения, изменения привязки номера телефона к адресу пользователя

## Running The Server

Рабочая директория `..\FastAPI-redis-etl`

Запустить команду после инициализации `.env` по образцу `env.example`

```bash
docker compose up -d --build
```

## Swagger

Url:

```
   http://localhost:8080/api/openapi
```

![user_info_service](docs/user_info_service.png)

## Running tests

Рабочая директория `..\FastAPI-redis-etl\data_app\tests\functional`

Запустить команду после инициализации `.env` по образцу `env.example`

```bash
docker compose up -d --build
```

# ETL

Рабочая директория `..\FastAPI-redis-etl\etl`

Запустить команду после инициализации `.env` по образцу `env.example`

```bash
docker compose up -d --build
```

Скрипт запустит PostgreSQL и созадние таблиц

Генерацию данных можно осуществить в `..\FastAPI-redis-etl\etl\init_db\data\generate_fake_data.py`

## Запросы

Проверка количества строк

```SQL
select count(distinct name)
from content.short_names

select count(distinct name)
from content.full_names
```

Решение 1

```SQL
WITH cte AS
(
	select fn.name, sn.status
	from content.full_names fn
	left join content.short_names sn on REGEXP_REPLACE(fn.name, '\.[^.]*$', '') = sn.name
)
update content.full_names
set status = cte.status 
from cte
where content.full_names.name = cte.name;
```

Проверка решения (разница между статусами должна быть 0)

```SQL
with cte as (
select fn.name, fn.status, sn.name, sn.status, sn.status - fn.status as difference_status
from content.full_names fn
left join content.short_names sn on REGEXP_REPLACE(fn.name, '\.[^.]*$', '') = sn.name
)
select *
from cte c
where c.difference_status > 0 or c.difference_status < 0


select *
from content.full_names fn 
where fn.status is null
```

Решение 2

Оформлено в качесте сравнения с SQL. В `etl/src/main.py`