number = int(input("Enter the number: "))
first_divisor = int(input("Enter the first divisor: "))
second_divisor = int(input("Enter the second divisor: "))
divisors = 0
if number % first_divisor == 0 and number % second_divisor == 0:
    divisors = 2
elif number % first_divisor == 0 or number % second_divisor == 0:
    divisors = 1
else:
    divisors = 0
print("\nDivisors: " + str(divisors))
