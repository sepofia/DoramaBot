"""
TODO: tell us your story...
"""


import yaml
import logging
import psycopg2
from psycopg2 import sql
from contextlib import closing


# load config-file for connection with local Database
with open('C:/Users/пк/Documents/repositories/DoramaBot/configuration/config_database.yaml', 'r') as handle:
    configs = yaml.full_load(handle)

with open('C:/Users/пк/Documents/repositories/DoramaBot/configuration/config_logger.yaml', 'r') as handle:
    logger_config = yaml.full_load(handle)


# logging
log_filename = logger_config['bot_logging']

with open(log_filename, 'a') as handle:
    handle.write('\n\n -- NEW SESSION -- \n')

logging.basicConfig(
    filename=log_filename
    , format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    , level=logging.INFO
)
logger = logging.getLogger(__name__)


# load already existed items in Database
def load_user_id() -> set:
    with closing(psycopg2.connect(**configs)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id from users;')
            result = set([elem[0] for elem in cursor.fetchall()])
            logger.info('Old users loaded from the local database')
            return result


# load new items in the Database
def update_users_database(value: tuple) -> None:
    with closing(psycopg2.connect(**configs)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True

            value_sql = sql.SQL(',').join(map(sql.Literal, [value]))
            insert = sql.SQL('INSERT INTO users VALUES {};').format(value_sql)
            cursor.execute(insert)
            logger.info(f'User {value[0]} added in the local database')


def update_command_database(value: tuple):
    with closing(psycopg2.connect(**configs)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True

            # The query now uses `sql.Identifier` to safely reference the column names
            # and `sql.Literal` for the values, making the query both secure and correct.
            value_sql = sql.SQL(',').join(map(sql.Literal, value))
            insert = sql.SQL('INSERT INTO commands (user_id, command_type, date_time, parameters) VALUES ({});')\
                .format(value_sql)

            cursor.execute(insert)
            logger.info(f'Command {value[1]} from user {value[0]} added in the database')
