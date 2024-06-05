import json
import logging
import os
import sys

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from psycopg2.extras import execute_batch

logging.basicConfig(
    stream=sys.stdout,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger('init_db')

DSN = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}

SCHEMA = "content"
SHORT_NAMES_TABLE = "short_names"
FULL_NAMES_TABLE = "full_names"


def create_db(pg_conn: _connection):
    logger.info("Инициализация БД")
    with pg_conn.cursor() as pg_curs:
        pg_curs.execute(
            f"""
                CREATE SCHEMA IF NOT EXISTS {SCHEMA};
                
                CREATE TABLE IF NOT EXISTS {SCHEMA}.{SHORT_NAMES_TABLE} (
                  "name" VARCHAR(100) PRIMARY KEY,
                  "status" INT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS {SCHEMA}.{FULL_NAMES_TABLE} (
                  "name" VARCHAR(100) PRIMARY KEY,
                  "status" INT
                );
            """
        )
        pg_conn.commit()
    logger.info("Инициализация БД завершена")


def read_json(name: str):
    with open(f"data/{name}.json") as json_data:
        data = json.load(json_data)
    return data


def insert_pg(pg_conn: _connection):
    with pg_conn.cursor() as pg_curs:
        for table in [SHORT_NAMES_TABLE, FULL_NAMES_TABLE]:
            logger.info(f"Заполнение данных для таблицы {table}")
            data = read_json(table)
            prepared_data = [tuple(row.values()) for row in data]
            query = f"""
                insert into {SCHEMA}.{table}
                values (%s, %s)
                on conflict (name) do nothing;
                COMMIT;
            """

            execute_batch(pg_curs, query, prepared_data, page_size=10_000)
            logger.info(f"Заполнение данных для таблицы {table} завершено")


if __name__ == "__main__":
    with psycopg2.connect(**DSN, cursor_factory=DictCursor) as pg_conn:
        create_db(pg_conn)
        insert_pg(pg_conn)
    pg_conn.close()
    logger.info(f"Таблицы инициализированны и заполнены данными")
