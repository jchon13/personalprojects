class PokeTeam:
    def __init__(self) -> None:
        self.battlemode = 0
        

    def choose_team(self,battle_mode: int,criterion: str = None) -> None:
        if (battle_mode > 2 or battle_mode < 0):
            raise ValueError('Battle Mode must be set as 0, 1 or 2')
        print('Howdy Trainer! Choose your team as C B S \n where C is the number of Charmanders \n B is the number of Bulbasaurs\n S is the number of Squirtles')
        holder = input()
        #print (int(holder[2])+int(holder[0])+int(holder[1]))
        #print(holder[1] == ' ')
        if (holder[1] != ' ' or holder[3] != ' '):
            return 'Use Appropriate Input Format'
        elif (int(holder[0])+int(holder[2])+int(holder[4]) > 6):
            return 'PokeTeams cannot be greater than 6'
        else:
            return self.assign_team(int(holder[0]),int(holder[2]),int(holder[4]))


    def assign_team(self,charm: int, bulb:int, squir: int) -> None:
        return 'WORKING'



a = PokeTeam()
print(a.choose_team(1,3))
