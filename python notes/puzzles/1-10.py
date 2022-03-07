def integerCheck(n:int) -> bool:
    counter_19 = 0
    counter_5 = 0
    for i in range(len(n)):
        if(n[i] == 19):
            counter_19 += 1
        elif( n[i]==5):
            counter_5 +=1
        else:
            pass
    
    if(counter_19 >= 2 and counter_5 >=3):
        return True


#print(integerCheck([19, 19, 15, 5, 3, 5, 5, 2]))


def fithEle(n:int) -> bool:
    counter = 0
    for i in range(len(n)):
        if(n[i] == n[5]):
            counter += 1
        else:
            pass
    if(len(n) == 8 and counter ==3):
        print(True)
    else:
        print(False)


fithEle([19, 15, 5, 7, 5, 5, 2])