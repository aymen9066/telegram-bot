from __future__ import annotations
from typing import Final
import module1.personne as personne, module1.composant as composant
from datetime import datetime


class Voiture:
    def __init__(self,model : str, production_year : int|None, brand : str, km : int = 0, utilisateur : personne.Personne | None = None, composants : list[composant.Composant] = []):
        self.model = model
        if self.is_production_year_valid(production_year):
            self.production_year = production_year
        else:
            self.production_year = None
        self.brand = brand
        self.km = km

    def is_production_year_valid(self, value : int|None) -> bool:
        if value is not None and 1970 <= value <= datetime.now().year:
            return True
        return False

    def __str__(self):
        return f"{self.brand} {self.model} produced in {self._production_year} driven for {self.km}km"
