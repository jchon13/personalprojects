from pokemon import Charmander, Bulbasaur, Squirtle


def battle(pk1, pk2) -> bool:
    # pk2 is taking damage, if True pk2 is dead
    pk2.calc_damage(pk1)
    if pk2.hp < 1:
        return True
    else:
        return False


c = Charmander()
b = Bulbasaur()

print(c)
print(b)

print(c.attack)

if c.speed > b.speed:
    print('c fast')
    if battle(c,b):
        print('b died')
        print(b.hp)
    else:
        if battle(b,c):
            print('c died')
            print(b.hp)
        else:
            print(b)
            print(c)