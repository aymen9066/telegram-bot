from __future__ import annotations
from abc import ABC, abstractmethod
import module1.voiture as voiture

class Composant(ABC):
    def __init__(self, state : bool):
        self.state = state
    def __str__(self):
        return f"{self.__class__.__name__} en {'bonne' if self.state else 'mauvaise'} etat "

class Moteur(Composant):
    def __init__(self, state : bool, cylinder_number : int, horse_power : int, torque : int):
        Composant.__init__(self, state)
        self.cylinder_number = cylinder_number
        self.horse_power = horse_power
        self.torque = torque

    def __str__(self):
        return Composant.__str__(self) + f" avec de {self.cylinder_number} cylindres et {self.horse_power} cheveaux et {self.torque} de torque."

class Pneu(Composant):
    def __init__(self, state : bool, width : int):
        Composant.__init__(self, state)
        self.width = width

    def __str__(self):
        return Composant.__str__(self) + f" avec diametre = {self.width}."

class Radiateur(Composant):
    def __init__(self, state : bool, temperature : int):
        Composant.__init__(self, state)
        self.temperature = temperature

    def __str__(self):
        return Composant.__str__(self) + f" avec temperature = {self.temperature}."