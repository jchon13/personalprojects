def insertionSort(array):
    for i in range(1,len(array)):
        key = array[i]

        j = i - 1
        #element 0 to i is sorted
        while j >= 0 and key > array[j]:
            array[j+1] = array[j]
            j -= 1
        array[j+1] = key


arr = [12,6,1,3,9]
insertionSort(arr)
print(arr)