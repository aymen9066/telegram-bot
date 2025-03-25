from __future__ import annotations
from abc import ABC, abstractmethod
import module1.voiture as voiture
from enum import StrEnum

class Personne(ABC):
    def __init__(self, chat_id : int, first_name : str , last_name : str , username : str, is_bot : bool, language_code : str,
                 voiture : voiture.Voiture | None = None):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.is_bot = is_bot
        self.language_code = language_code
        self.voiture = voiture
        self.role = "client"

    def store_db(self, connection):
        cursor = connection.cursor()
        cursor.execute("insert into users(chat_id, first_name, last_name, username, is_bot, language_code, role)"
        " values(%s, %s, %s , %s, %s, %s, %s)"
        " on conflict (chat_id) do nothing"
        ,({self.chat_id}, {self.first_name}, {self.last_name}, {self.username}, {self.is_bot}, {self.language_code if self.language_code else 'fr'}, {self.role}) )
        cursor.execute("insert into car_listing")

class Client(Personne):
    def become_mecanique(self):
        ...

class Mecanicien(Personne):
    def __init__(self, chat_id : int, first_name : str , last_name : str , username : str, is_bot : bool, language_code : str
                 ,password : str,voiture : voiture.Voiture | None = None):
        super().__init__(chat_id, first_name, last_name, username, is_bot, language_code, voiture)
        self.password = password
        self.role = "mecanicien"
