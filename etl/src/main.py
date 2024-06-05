import datetime
import logging
import os
import sys

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_batch

logging.basicConfig(
    stream=sys.stdout,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger('etl')

DSN = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}


class ETL:
    state: str | None = None

    def __init__(self, pg_conn: _connection):
        self.pg_conn = pg_conn

    def get_state(self, pg_cur):
        pg_cur.execute(
            """
                SELECT name, status
                FROM content.short_names
                ORDER BY name
                limit 1
            """
        )
        return pg_cur.fetchall()[0][0]

    def produce(self):
        started = False
        with self.pg_conn.cursor() as cur:
            self.state = self.get_state(cur)
            cur.execute(
                """
                    SELECT name, status
                    FROM content.short_names
                    WHERE name >= %s
                    ORDER BY name
                """,
                [self.state]
            )
            while results := cur.fetchmany(100000):
                res_dict = {row[0]: row[1] for row in results}
                with self.pg_conn.cursor(cursor_factory=DictCursor) as cur_:
                    names = tuple(res_dict.keys())
                    cur_.execute(
                        f"""
                            SELECT
                                fn.status,
                                fn.name
                            FROM content.full_names fn
                            WHERE REGEXP_REPLACE(fn.name, '\.[^.]*$', '') IN {names}
                        """
                    )
                    transform_data = cur_.fetchall()
                for this_row in transform_data:
                    this_name = this_row[1].split('.')[0]
                    if this_name in res_dict:
                        this_row[0] = res_dict[this_name]

                transform_data = [tuple(row) for row in transform_data]
                with self.pg_conn.cursor() as cur__:
                    query = """
                        UPDATE content.full_names
                        SET status=%s
                        WHERE name=%s;
                    """
                    print(1)
                    execute_batch(cur__, query, transform_data, page_size=50000)


if __name__ == "__main__":
    now = datetime.datetime.now()
    with psycopg2.connect(**DSN) as pg_conn:
        ETL(pg_conn).produce()
    pg_conn.close()
    print(datetime.datetime.now() - now)
    # порядка 0:01:15.229734
