import psycopg2
from config import *

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

conn.autocommit = True


def create_table_users():
    with conn.cursor() as cursor:
        cursor.execute('CREATE TABLE IF NOT EXISTS users('
                       'id serial, '
                       'user_id varchar(20) NOT NULL PRIMARY KEY);')
        print('Таблица users создана')


def create_table_people(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS people{user_id}('
                       'id serial,'
                       'f_name varchar(40) NOT NULL,'
                       'l_name varchar(40) NOT NULL,'
                       'vk_id varchar(20) NOT NULL PRIMARY KEY,'
                       'vk_link varchar(60));')
    print('Таблица people создана')


def create_table_seen_people(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS seen_people{user_id} ('
                       'id serial,'
                       'vk_id varchar(20) PRIMARY KEY);')
    print('Таблица seen_people создана')


def insert_user(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO users (user_id) VALUES ('{user_id}');")


def insert_people(user_id, f_name, l_name, vk_id, vk_link):
    first_name = f_name.replace("'", "")
    last_name = l_name.replace("'", "")
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO people{user_id} (f_name, l_name, vk_id, vk_link) "
                       f"VALUES ('{first_name}', '{last_name}', '{vk_id}', '{vk_link}');")


def insert_seen_people(user_id, vk_id):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO seen_people{user_id} (vk_id) VALUES ('{vk_id}');")


def select_users():
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM users;')
        return cursor.fetchall()


def select(user_id, offset):
    with conn.cursor() as cursor:
        cursor.execute(f'SELECT u.f_name, u.l_name, u.vk_id, u.vk_link, su.vk_id '
                       f'FROM people{user_id} AS u '
                       f'LEFT JOIN seen_people{user_id} AS su '
                       f'ON u.vk_id = su.vk_id WHERE su.vk_id IS NULL '
                       f'OFFSET {offset};')
        return cursor.fetchone()


def drop_table_users():
    with conn.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS users CASCADE;')


def drop_people(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS people{user_id} CASCADE;')
        print('Таблица people удалена')


def drop_seen_people(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS seen_people{user_id} CASCADE')
        print('Таблица seen_people удалена')


def create_db(user_id):
    drop_people(user_id)
    drop_seen_people(user_id)
    create_table_people(user_id)
    create_table_seen_people(user_id)
