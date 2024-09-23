import psycopg2
from myconfig import *

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


def insert_users(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO users (user_id) VALUES ('{user_id}');")


def create_table_persons():
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS people ('
                       'id serial, '
                       'user_id varchar(20), '
                       'f_name varchar(40) NOT NULL, '
                       'l_name varchar(40) NOT NULL, '
                       'vk_id varchar(20) NOT NULL, '
                       'vk_link varchar(60), '
                       'PRIMARY KEY (user_id, vk_id));')
    print('Таблица people создана')


def insert_people(user_id, f_name, l_name, vk_id, vk_link):
    first_name = f_name.replace("'", "")
    last_name = l_name.replace("'", "")
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO people (user_id, f_name, l_name, vk_id, vk_link) "
                       f"VALUES ('{user_id}', '{first_name}', '{last_name}', '{vk_id}', '{vk_link}');")


def delete_from_people(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f"DELETE FROM people "
                       f"WHERE user_id = '{user_id}'")


def create_table_seen_people():
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS seen_people ('
                       'id serial, '
                       'user_id varchar(20), '
                       'vk_id varchar(20), '
                       'PRIMARY KEY (user_id, vk_id));')
    print('Таблица seen_people создана')


def insert_seen_people(user_id, vk_id):
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO seen_people (user_id, vk_id) VALUES ('{user_id}', '{vk_id}');")


def delete_from_seen_people(user_id):
    with conn.cursor() as cursor:
        cursor.execute(F"DELETE FROM seen_people "
                       F"WHERE user_id = '{user_id}'")


def select_users():
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM users;')
        return cursor.fetchall()


def select(user_id):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT u.user_id, u.f_name, u.l_name, u.vk_id, u.vk_link, su.vk_id "
                       f"FROM people AS u "
                       f"LEFT JOIN seen_people AS su "
                       f"ON u.vk_id = su.vk_id and u.user_id = su.user_id "
                       f"WHERE su.vk_id IS NULL and u.user_id = '{user_id}';")
        return cursor.fetchone()


def drop_users():
    with conn.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS users CASCADE;')
        print('Таблица users удалена')


def drop_people():
    with conn.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS people CASCADE;')
        print('Таблица people удалена')


def drop_seen_people():
    with conn.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS seen_people CASCADE;')
        print('Таблица seen_people удалена')


def create_db():
    drop_users()
    drop_people()
    drop_seen_people()
    create_table_users()
    create_table_people()
    create_table_seen_people()


