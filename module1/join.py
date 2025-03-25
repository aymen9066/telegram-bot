import psycopg, os
from abc import ABC
from flask.cli import load_dotenv
from datetime import datetime

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

class Personne(Storable, ABC):
    def __init__(self, chat_id: int, first_name: str, last_name: str, username: str, is_bot: bool, language_code: str):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.is_bot = is_bot
        self.language_code = language_code
        self.role = "client"
        self.store_db()

    def store_db(self):
        cursor = Storable.connection.cursor()
        cursor.execute("insert into users(chat_id, first_name, last_name, username, is_bot, language_code, role)"
                       " values(%s, %s, %s , %s, %s, %s, %s)"
                       " on conflict (chat_id) do update "
                       "set first_name = excluded.first_name and last_name = excluded.last_name and username = excluded.username and language_code = excluded.language_code"
                       , ({self.chat_id}, {self.first_name}, {self.last_name}, {self.username}, {self.is_bot},
                          {self.language_code if self.language_code else 'fr'}, {self.role}))

    def __str__(self):
        return f"{self.__class__.__name__} {self.first_name},{self.last_name} avec chat_id = {self.chat_id} et username = {self.username} et is_bot = {self.is_bot} et lang = {self.language_code}"


class Client(Personne):
    def __init__(self, chat_id: int, first_name: str, last_name: str, username: str, is_bot: bool, language_code: str):
        Personne.__init__(self, chat_id, first_name, last_name, username, is_bot, language_code)
        self.store_db()
    def become_mecanique(self):
        ...


class Mecanicien(Personne):
    def __init__(self, chat_id: int, first_name: str, last_name: str, username: str, is_bot: bool, language_code: str, password: str):
        Personne.__init__(self,chat_id, first_name, last_name, username, is_bot, language_code)
        self.password = password
        self.role = "mecanicien"

class Voiture(Storable):
    def __init__(self,model : str, production_year : int|None, brand : str, km : int = 0, user : Personne | None = None):
        self.model = model
        if self.is_production_year_valid(production_year):
            self.production_year = production_year
        else:
            self.production_year = None
        self.brand = brand
        self.km = km
        self.user = user

    def is_production_year_valid(self, value : int|None) -> bool:
        if value is not None and 1970 <= value <= datetime.now().year:
            return True
        return False
    def store_db(self):
        cursor = Storable.cursor()
        id = cursor.execute(f"select id,name from car_brand where name = {self.brand}").fetchone()
        if not id:
            cursor.execute("insert into car_brand(name) values(%s) returning id", ({self.brand}))
            brand_id = cursor.fetchone()[0]
        else:
            brand_id = id[0]
        id = cursor.execute(f"select id,name from car_model where name = {self.model}").fetchone()
        if not id:
            cursor.execute("insert into car_model(id_brand, name, production_year) values(%s, %s, %s) returning id"
                           , (brand_id , {self.model}, {self.production_year}))
            model_id = cursor.fetchone()[0]
        else:
            model_id = id[0]
        car_id = cursor.execute("insert into cars(id_model, km_dirven) values(%s,%s) returning id" ,(model_id, {self.km})).fetchone()
        user_id = cursor.execute(f"select id from users where chat_id = {self.user.chat_id}").fetchone()[0]
        cursor.execute("insert into car_listing values(%s, %s)", (car_id[0], user_id[0]))

    def __str__(self):
        return f"{self.brand} {self.model} produced in {self._production_year} driven for {self.km}km"

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

x = cursor.execute(f"select chat_id from users where chat_id = 123").fetchone()
#u1 = personne.Client(141651621, "Akram", "Salama", "Akram3151", False, "ar")
if x:
    print("element found")
    print(x[0])
else:
    print("element not found")
