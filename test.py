def binary_search(the_list, target, low, high):
    if low > high:
        return -1
    else:
        mid = (high + low) // 2
    if the_list[mid] == target:
        return mid
    elif the_list[mid] > target:
        return binary_search(the_list, target, low, mid - 1)
    else:
        return binary_search(the_list, target, mid + 1, high)


def main() -> None:
    arr = [1, 5, 10, 11, 12]
    index = binary_search(arr, 11, 0, len(arr) - 1)
    print(index)


main()