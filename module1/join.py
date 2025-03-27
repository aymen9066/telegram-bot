from __future__ import annotations
import os, requests, json
from abc import ABC
from datetime import datetime
from telegram import User as telegramUser

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
        self.cars : list[Voiture] = []

    def store_db(self):
        self.id = insert_user(self.chat_id ,self.first_name, self.last_name, self.username, self.is_bot, self.language_code if self.language_code is not None else "fr", self.role)

    def __str__(self):
        return f"{self.__class__.__name__} {self.first_name},{self.last_name} avec chat_id = {self.chat_id} et username = {self.username} et is_bot = {self.is_bot} et lang = {self.language_code} et id = {self.id}"

    def find_cars(self) -> int:
        print("enter finding the car...")
        cursor = Storable.connection.cursor()
        rows = cursor.execute(f"select id_car from car_listing where id_user = {self.id}").fetchall()
        for row in rows:
            print("voiture trouve en find cars...")
            voiture = Voiture.createFromId(row[0], self)
            assert(voiture is not None)
            if voiture not in self.cars:
                self.cars.append(voiture)
        return len(rows)


class Client(Personne):
    def __init__(self, chat_id: int, first_name: str, last_name: str|None, username: str|None, is_bot: bool, language_code: str|None):
        Personne.__init__(self, chat_id, first_name, last_name, username, is_bot, language_code)
        self.store_db()

    @staticmethod
    def create_from_telegram_user(chat_id : int, user : telegramUser) -> Personne:
        return Client(chat_id, user.first_name, user.last_name, user.username, user.is_bot, user.language_code)

class Mecanicien(Personne):
    def __init__(self, chat_id: int, first_name: str, last_name: str, username: str, is_bot: bool, language_code: str, password: str):
        Personne.__init__(self,chat_id, first_name, last_name, username, is_bot, language_code)
        self.password = password
        self.role = "mecanicien"
        self.store_db()

class Voiture(Storable):
    def __init__(self, brand : str , model : str, production_year : int|None, km : int = 0, user : Personne | None = None):
        self.brand = brand
        self.model = model
        if Voiture.is_production_year_valid(production_year):
            self.production_year = production_year
        else:
            self.production_year = None
        self.km = km
        self.user = user
        self.store_db()

    @staticmethod
    def createFromId(id_car : int, user : Personne|None = None) -> Voiture|None:
        data = (Storable.connection.execute(f"select car_brand.name,car_model.name,car_model.production_year, cars.km_dirven "
                f"from cars,car_model,car_brand "
                f"where cars.id = {id_car} and car_model.id = cars.id_model and car_brand.id = car_model.id_brand")
              .fetchone())
        if data:
            return Voiture(brand = data[0],model = data[1],production_year=data[2],km=data[3], user=user)
        return None

    @staticmethod
    def is_production_year_valid(value : int|None) -> bool:
        if value is not None and 1970 <= value <= datetime.now().year:
            print("production year is valid")
            return True
        print(f"production year is not valid p = {value} and now is {datetime.now().year}!")
        return False

    def store_db(self):
        cursor = Storable.connection.cursor()
        brand_id = insert_car_brand(self.brand)
        model_id = insert_car_model(brand_id, self.model, self.production_year)
        car_id = insert_car(model_id, self.km)
        user_id = cursor.execute(f"select id from users where chat_id = {self.user.chat_id}").fetchone()[0]
        insert_car_listing(car_id, user_id)

    def __str__(self):
        return f"{self.brand} {self.model} produced in {self.production_year} driven for {self.km}km"

class Model:
    default_init_message = "Tu es un expert en diagnostic des vehicules, soyer concis dans votre responce et preferer des reponses en moins d'une paragraphe."
    supported_models = ["deepseek"]
    def __init__(self, name : str, api_key : str, openrouter_name : str, init_message : str = ""):
        self.name = name
        self.api_key = api_key
        self.__openrouter_name = openrouter_name
        self.contex : list[dict[str,str]] = []
        self.personal_context : dict[str,str] = {"car" : "", "engine" : ""}
        self.init_message = Model.default_init_message if init_message == "" else init_message
        self.contex.append({"role": "system", "content" : self.init_message})

    @staticmethod
    def create(name : str, chat_id : int, init_message : str = "") -> Model:
        api_key = os.getenv(f"{name}_key")
        if api_key is None:
            raise ValueError(f"Erreur : {name} api key env variable not found!")
        if name == "deepseek":
            model = Model(name, api_key, "deepseek/deepseek-chat:free", init_message)
        else:
            raise ValueError(f"Cannot create the model because {name} is not supported!\nSupported models are {Model.supported_models}")
        model.get_contex_from_db(chat_id)
        return model

    def prompt(self, message : str, with_context : bool = True):
        for key in self.personal_context:
            if self.personal_context[key] != "":
                message = self.personal_context[key] + ", " + message

        if not with_context:
            self.contex.append({"role":"user","content" : message})
            messages = self.contex
        else:
            messages = [{"role":"user", "content": message}]
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": self.__openrouter_name,
                "messages": messages,
            })
        )
        response_content = response.json().get('choices')[0].get('message').get('content')
        self.contex.append({"role": "assistant", "content" : response_content})
        return response_content

    def get_contex_from_db(self, chat_id : int) -> None:
        cursor = Storable.connection.cursor()
        message_rows = cursor.execute(f"select is_bot, content from message_view where chat_id = {chat_id} order by number").fetchall()
        for message_row in message_rows:
            self.contex.append({"role": "user" if message_row[0] else "assistant", "content" : message_row[1]})

