#defining a function calculating n!

def factorial(num):
    if num <= 1:
        return 1
    
    return num * factorial(num - 1)

print(factorial(5)) #120

# another way using for loop for calculating 10!

prod = 1
for num in range(1, 11):
    prod *= num

print(prod)
