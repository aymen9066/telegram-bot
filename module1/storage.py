from __future__ import annotations
from abc import ABC
import psycopg, os
from flask.cli import load_dotenv

load_dotenv()
class Storable(ABC):
    db_user = os.getenv("db_user")
    if db_user is None:
        raise ValueError("can't find env variable db_user!")
    db_password = os.getenv("db_password")
    if db_password is None:
        raise ValueError("can't find env variable db_password!")
    connection = psycopg.connect(f"dbname={db_user} user={db_user} password={db_password} host=localhost")
    connection.autocommit = True
    cursor = connection.cursor()
    f =  open(os.path.dirname(os.path.realpath(__file__))+ "/tables.sql", "r")
    sql_commands = f.read()
    cursor.execute(sql_commands)
    cursor.close()

    @staticmethod
    def insert_message(chat_id : int, user_id : int, message_id : int, content : str):
        cursor = Storable.connection.cursor()
        cursor.execute("insert into chats(id) values(%s) on conflict (id) do nothing", (chat_id,))
        cursor.execute("insert into chat_users(chat_id, user_id) values(%s,%s) "
                       "on conflict (chat_id) do nothing", (chat_id, user_id))
        cursor.execute("insert into messages(chat_id, user_id, number, content) values(%s,%s,%s,%s)"
                       , (chat_id, user_id, message_id, content))


def insert_car_brand(car_brand) -> int:
    cursor = Storable.connection.cursor()
    id = cursor.execute(f"select id from car_brand where name = '{car_brand}'").fetchone()
    if not id:
        id = cursor.execute("insert into car_brand(name) values(%s) returning id", (car_brand,)).fetchone()
        if id is None:
            raise ValueError("insertion of car brand failed!")
        return id[0]
    return id[0]

def insert_car_model(id_brand : int, car_model : str, production_year : int) -> int:
    cursor = Storable.connection.cursor()
    id = cursor.execute(f"select id from car_model where id_brand = {id_brand} and name = '{car_model}' and production_year = {production_year}").fetchone()
    if not id:
        id = cursor.execute("insert into car_model(id_brand, name, production_year) values(%s,%s,%s) returning id"
                   ,(id_brand, car_model, production_year)).fetchone()
        if id is None:
            raise ValueError("insertion of car model failed!")
        return id[0]
    return id[0]

def insert_car(id_model : int, km_driven : int) -> int:
    cursor = Storable.connection.cursor()
    id = cursor.execute(f"select id from cars where id_model = {id_model} and km_dirven = {km_driven}").fetchone()
    if not id:
        id = cursor.execute("insert into cars(id_model, km_dirven) values(%s, %s) returning id", (id_model, km_driven)).fetchone()
        if id is None:
            raise ValueError("insertion of car failed!")
        return id[0]
    return id[0]


def insert_car_listing(id_car : int, id_user : int) -> None:
    cursor = Storable.connection.cursor()
    if not cursor.execute(f"select id_car from car_listing where id_car = {id_car} and id_user = {id_user}").fetchone():
        cursor.execute("insert into car_listing(id_car, id_user) values(%s, %s)", (id_car, id_user))

def insert_user(chat_id : int, first_name : str, last_name : str|None, username : str|None, is_bot : bool, language_code : str|None, role : str) -> int:
    cursor = Storable.connection.cursor()
    id = cursor.execute("insert into users(chat_id, first_name, last_name, username, is_bot, language_code, role) values(%s, %s,%s,%s,%s,%s,%s)"
                    " on conflict (chat_id) do update set first_name=excluded.first_name, last_name=excluded.last_name, username=excluded.username, is_bot=excluded.is_bot, language_code=excluded.language_code, role=excluded.role"
                    " returning id", (chat_id, first_name, last_name, username, is_bot, language_code, role)).fetchone()
    if id is None:
        raise ValueError("insertion of user failed!")
    return id[0]