
# @author Vaclav Kral xkralva00

# Matematické operace pro výpočet sčítaní
def add(a,b):
    return a + b

# Matematická operace pro výpočet odčítaní
def subtract(a,b):
    return a - b

# Matematická operace pro výpočet násobení
def multiply(a,b):
    return a * b

# Matematická operace pro výpočet dělení
def divide(a,b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

# Matematická operace pro výpočet mocniny
def power(a,b):
    if a == 0 and b < 0:
        raise ValueError("Cannot raise zero to a negative power")
    return a ** b

# Matematická operace pro výpočet odmocniny
def root(a, b):
    if b == 0:
        raise ValueError("Root degree cannot be zero")
    if b < 0:
        raise ValueError("Cannot compute square root with a negative degree")
    if a < 0 and b % 2 == 0:
        raise ValueError("Cannot compute square root of a negative number")
    if a == 0 and b == 0:
         raise ValueError("Cannot compute 0th root of 0")
    return a ** (1 / b)

# Matematická operace pro výpočet faktoriálu
def factorial(n):
    if not isinstance(n, int):
        raise ValueError("Factorial is only defined for integers")
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

# Matematická operace pro výpočet absolutní hodnoty  
def absolute_value(x):
    return abs(x)

# Funkce pro vyhodnocení matematického výrazu
def evaluate(expression):
    allowed_names = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'power': power,
        'root': root,
        'factorial': factorial,
        'absolute_value': absolute_value,
        }

    return eval(expression, {"__builtins__": None}, allowed_names)
