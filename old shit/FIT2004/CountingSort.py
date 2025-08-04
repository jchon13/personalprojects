def countingSort(array):
    output = [0]*len(array)
    
    #count array
    count = [0] * 10
    
    #Store count of each element in array
    for i in range(0,len(array)):
        count[array[i]] += 1

    #Change count to display position
    for i in range(10):
        count[i] += count[i-1]

    #Build output 
    for i in range(len(array)):
        print(count[array[i]]-1)
        output[count[array[i]]-1] = array[i]
        print(output)
        
        count[array[i]] -= 1

    #Copy output to array 
    for i in range(0,len(array)):
        array[i] = output[i]


data = [4,2,2,8,3,3,1]
countingSort(data)
print(data)
