from poke_team import PokeTeam


class Battle:
    def __init__(self,trainer_one_name: str, trainer_two_name: str) -> None:
        self.trainer_one = trainer_one_name
        self.trainer_two = trainer_two_name

    def set_mode_battle(self) -> str:
        self.trainer_one = PokeTeam(self.trainer_one)
        self.trainer_two = PokeTeam(self.trainer_two)
        self.trainer_one.choose_team(0,None)
        self.trainer_two.choose_team(0,None)
        

        #while length of both trainers is not zero rounds will go
        #checks speed of first pokemon in party to determine attackers and defender
        #after each attack checks if a pokemon has fainted if so remove it
        #if a pokemon has fainted end the round
        #when the loop ends return result 


        while self.trainer_one.team.length != 0 or self.trainer_two.team.length != 0:
            pk_1 = self.trainer_one.team.peek()
            pk_2 = self.trainer_two.team.peek()
            
            if pk_1.speed > pk_2.speed:
                
                if self.battle(pk_1, pk_2):
                    
                    self.trainer_two.team.serve()
                else:
                    if self.battle(pk_2,pk_1):
                        self.trainer_one.team.serve()
                    else:
                        self.update(pk_1,pk_2)
            elif pk_1.speed < pk_2.speed:
                
                if self.battle(pk_2, pk_1):
                    self.trainer_one.team.serve()
                else:
                    if self.battle(pk_1,pk_2):
                        self.trainer_two.team.serve()
                    else:
                        self.update(pk_1,pk_2)
            elif pk_1.speed == pk_2.speed:
                
                if self.battle(pk_2, pk_1):
                    self.trainer_one.team.serve()
                    continue
                elif self.battle(pk_1, pk_2):
                    self.trainer_two.team.serve()
                else:
                    self.update(pk_1,pk_2)

            
            if self.trainer_one.team.length == 0 or self.trainer_two.team.length == 0:
                break

        if self.trainer_one.team.length == 0 and self.trainer_two.team.length ==0:
            return 'Draw'
        elif self.trainer_one.team.length == 0:
            return self.trainer_two.trainer_name
        elif self.trainer_two.team.length == 0:
            return self.trainer_one.trainer_name
        else: pass
      


    

    def battle(self,pk1,pk2) -> bool:
        #pk2 is taking damage, if True pk2 is dead
        pk2.calc_damage(pk1)
        if pk2.hp < 1: 
            return True
        else:
            return False
    
    def update(self,pk1,pk2) -> None:
        self.trainer_one.team.array[self.trainer_one.team.front] = pk1
        self.trainer_two.team.array[self.trainer_two.team.front] = pk2
                


a = Battle('Ash','Misty')
print(a.set_mode_battle())
