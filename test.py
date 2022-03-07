def mystery(n):
    count = 0
    add =0
    i = 0
    while i < len(n):
        add = add + n[i]
        j = 0
        while j < len(n):
            add = add + n[j]
            j = j + 1
        i = i + 1
    
    print(add)

mystery([1,2,3,4,5,6,7])