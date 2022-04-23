'''This file contains python code for calculating the
number of multiples of a given number from a given
list of integers
"""
__author__ = "Saksham Nagpal"
__date__ = "01.08.2021"
'''
from typing import List


def get_multiples(the_list: List[int], n: int) -> int:
    """
    Computes the number of multiples of n
    :pre: n > 0
    :param the_list: The list of integers being passed
    :param n: The number to check for multiples
    :returns: the count of multiples from the list
    """
    count = 0             # Initialise counter as 0
    for i in range(len(the_list)):    # Loop through the_list
        if the_list[i] % n == 0 and the_list[i] != n:  # If that element is not n but is divisible by n,
            count += 1                                 # increment count
    return count


def main() -> None:
    my_list = [2, 4, 6]
    n = 3
    print("The number of multiples of " + str(n) + " is: " + str(get_multiples(my_list, n)))


main()