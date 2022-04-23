from pokemon_base import PokemonBase as PB

class Charmander(PB):
    def __init__(self) -> None:
        PB.__init__(self,7,'Fire')
        self.attack = 6 + self.level
        self.defence = 4
        self.speed = 7 + self.level

    def get_hp_and_level(self) -> int:
        return 'Charmander\'s HP = ' + str(self.hp) + ' and level = ' + str(self.level)

    def set_hp(self,hp) -> None:
        self.hp = hp

    def set_level(self,level) -> None:
        self.level = level

    #name, speed, attackand poke_type of the Pokemon
    def get_stats(self):
        return 'Charmander\'s, Speed = ' + str(self.speed) + ', Attack = ' + str(self.attack) + ', Type = ' + str(self.poke_type)

    def calc_damage(self,damage) -> int:
        if damage > self.defence:
            self.hp = self.hp - damage
        else:
            self.hp = self.hp - damage//2
        return self.hp


class Bulbasaur(PB):
    def __init__(self) -> None:
        PB.__init__(self,9,'Grass')
        self.attack = 5
        self.defence = 5
        self.speed = 7 + (self.level //2)


    def get_hp_and_level(self) -> int:
        return 'Bulbasaur\'s HP = ' + str(self.hp) + ' and level = ' + str(self.level)

    def set_hp(self,hp) -> None:
        self.hp = hp

    def set_level(self,level) -> None:
        self.level = level

    #name, speed, attackand poke_type of the Pokemon
    def get_stats(self):
        return 'Bulbasaur\'s, Speed = ' + str(self.speed) + ', Attack = ' + str(self.attack) + ', Type = ' + str(self.poke_type)

    def calc_damage(self,damage) -> int:
        if damage > self.defence + 5:
            self.hp = self.hp - damage
        else:
            self.hp = self.hp - damage//2
        return self.hp
    
class Squirtle(PB):
    def __init__(self) -> None:
        PB.__init__(self,8,'Water')
        self.attack = 4 + self.level//2
        self.defence = 6 + self.level
        self.speed = 7 


    def get_hp_and_level(self) -> int:
        return 'Squirtle\'s HP = ' + str(self.hp) + ' and level = ' + str(self.level)

    def set_hp(self,hp) -> None:
        self.hp = hp

    def set_level(self,level) -> None:
        self.level = level

    #name, speed, attackand poke_type of the Pokemon
    def get_stats(self):
        return 'Squirtle\'s, Speed = ' + str(self.speed) + ', Attack = ' + str(self.attack) + ', Type = ' + str(self.poke_type)

    def calc_damage(self,damage) -> int:
        if damage > self.defence*2:
            self.hp = self.hp - damage
        else:
            self.hp = self.hp - damage//2
        return self.hp


a = Squirtle()
print(a.get_hp_and_level())
print(a.set_hp(50))
print(a.get_hp_and_level())
