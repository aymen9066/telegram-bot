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
    cursor = connection.cursor()
    f =  open(os.path.dirname(os.path.realpath(__file__))+ "/tables.sql", "r")
    sql_commands = f.read()
    cursor.execute(sql_commands)
