from abc import ABC, abstractmethod

class PokemonBase(ABC):
    def __init__(self,hp,poke_type) -> None:
        self.level = 1
        self.hp = hp
        self.poke_type = poke_type

    @abstractmethod
    def get_hp_and_level(self) -> str:
        pass

    def set_hp(self,hp) -> None:
        self.hp = hp

    def set_level(self,level) -> None:
        self.level = level

    @abstractmethod
    def get_stats(self) -> str:
        pass

    @abstractmethod
    def calc_damage(self) -> int:
        pass

