from __future__ import annotations
from abc import ABC, abstractmethod
from enum import StrEnum
import module1.storage


class Personne(module1.storage.Storable, ABC):
    def __init__(self, chat_id: int, first_name: str, last_name: str, username: str, is_bot: bool, language_code: str):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.is_bot = is_bot
        self.language_code = language_code
        self.role = "client"
        self.voitures : list = []
        self.store_db()

    def store_db(self):
        cursor = module1.storage.Storable.connection.cursor()
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

