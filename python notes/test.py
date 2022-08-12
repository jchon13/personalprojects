string = '1 1 1'


while True:
    holder = input()
    if (holder[1] != ' ' or holder[3] != ' '):
        print('entered one')
        print('Use Appropriate Input Format')
    elif (int(holder[0])+int(holder[2])+int(holder[4]) > 6):
            print('PokeTeams cannot be greater than 6')
            print('entered two')
    else:
        print('works')
        break        
