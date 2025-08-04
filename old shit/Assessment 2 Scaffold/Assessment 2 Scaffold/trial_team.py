from queue_adt import CircularQueue
from stack_adt import ArrayStack
from pokemon import Charmander, Bulbasaur,Squirtle




class PokeTeam:
    def __init__(self,name:str) -> None:
        self.battlemode = 0
        self.trainer_name = name
        self.team = None
        

    def choose_team(self,battle_mode: int,criterion: str = None) -> None:
        if (battle_mode > 2 or battle_mode < 0):
            raise ValueError('Battle Mode must be set as 0, 1 or 2')
        print('Howdy Trainer! Choose your team as C B S \n where C is the number of Charmanders \n B is the number of Bulbasaurs\n S is the number of Squirtles')
        self.battlemode = battle_mode
        #print (int(holder[2])+int(holder[0])+int(holder[1]))
        #print(holder[1] == ' ')
        while True:
            holder = input()
            if (holder[1] != ' ' or holder[3] != ' '):
                print('Use Appropriate Input Format')
            elif (int(holder[0])+int(holder[2])+int(holder[4]) > 6):
                print('PokeTeams cannot be greater than 6')
            elif (int(holder[0])+int(holder[2])+int(holder[4]) < 1):
                print('PokeTeams must have at least one pokemon')
            else:
                self.assign_team(int(holder[0]),int(holder[2]),int(holder[4]))
                break


    def assign_team(self,charm: int, bulb:int, squir: int) -> None:
        if self.battlemode == 0:
            self.team = ArrayStack(6)
            for i in range(squir):
                self.team.push(Squirtle())
                #print('squir')
            for i in range(bulb):
                self.team.push(Bulbasaur())
                #print('bulb')
            for i in range(charm):
                self.team.push(Charmander())
                #print('charm')
            
        elif self.battlemode == 1:
            self.team = CircularQueue(6)
            for i in range(charm):
                self.team.append(Charmander())
                #print('charm')
            for i in range(bulb):
                self.team.append(Bulbasaur())
                #print('bulb')
            for i in range(squir):
                self.team.append(Squirtle())
                #print('squir')
        else: 
            pass

        

    def __str__(self):
        output = '' 
        holder = self.team
        if self.battlemode == 0:
            for i in range(self.team.length):
                output += str(holder.pop())
                output += ', '
            
        elif self.battlemode == 1:
            for i in range(self.team.length):
                output += str(holder.serve())
                output += ', '
        else:
            pass
        output = output[:-2]
        return output 

        #return 'Charmander\'s HP = 7 and level = 1, Bulbasaur\'s HP = 9 and level = 1, Squirtle\'s HP = 8 and level = 1'
        
