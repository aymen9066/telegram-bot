from abc import ABC
import psycopg, os

class Storable(ABC):
    user = os.getenv("db_user")
    if user is None:
        raise ValueError("can't find env variable db_user!")
    password = os.getenv("db_password")
    if password is None:
        raise ValueError("can't find env variable db_password!")
    connection = psycopg.connect(f"dbname={user} user={user} password={password} host=localhost")
    cursor = connection.cursor()
    with open("module1/tables.sql", "r") as f:
        sql_commands = f.read()
    cursor.execute(sql_commands)
