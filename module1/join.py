from abc import ABC
from datetime import datetime
from module1.storage import *

class Personne(Storable, ABC):
    def __init__(self, chat_id: int, first_name: str, last_name: str|None, username: str|None, is_bot: bool, language_code: str|None):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.is_bot = is_bot
        self.language_code = language_code
        self.role = "client"

    def store_db(self):
        self.id = insert_user(self.chat_id, self.first_name, self.last_name, self.username, self.is_bot, self.language_code if self.language_code is not None else "fr", self.role)

    def __str__(self):
        return f"{self.__class__.__name__} {self.first_name},{self.last_name} avec chat_id = {self.chat_id} et username = {self.username} et is_bot = {self.is_bot} et lang = {self.language_code}"


class Client(Personne):
    def __init__(self, chat_id: int, first_name: str, last_name: str, username: str, is_bot: bool, language_code: str):
        Personne.__init__(self, chat_id, first_name, last_name, username, is_bot, language_code)
        self.store_db()

class Mecanicien(Personne):
    def __init__(self, chat_id: int, first_name: str, last_name: str, username: str, is_bot: bool, language_code: str, password: str):
        Personne.__init__(self,chat_id, first_name, last_name, username, is_bot, language_code)
        self.password = password
        self.role = "mecanicien"
        self.store_db()

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
        self.store_db()

    def is_production_year_valid(self, value : int|None) -> bool:
        if value is not None and 1970 <= value <= datetime.now().year:
            return True
        return False

    def store_db(self):
        cursor = Storable.connection.cursor()
        brand_id = insert_car_brand(self.brand)
        model_id = insert_car_model(brand_id, self.model, self.production_year)
        car_id = insert_car(model_id, self.km)
        user_id = cursor.execute(f"select id from users where chat_id = {self.user.chat_id}").fetchone()[0]
        insert_car_listing(car_id, user_id)

    def __str__(self):
        return f"{self.brand} {self.model} produced in {self._production_year} driven for {self.km}km"