from __future__ import annotations
from typing import Final
import module1.personne as Per
from datetime import datetime
import module1.storage



class Voiture(module1.storage.Storable):
    def __init__(self,model : str, production_year : int|None, brand : str, km : int = 0, user : Per.Personne | None = None):
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
        cursor = module1.storage.Storable.cursor()
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
