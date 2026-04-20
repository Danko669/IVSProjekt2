##
# @file mathematic.py
# @brief Matematická knihovna pro základní operace
# @author Václav Král xkralva00
# @date 2026-04-02

##
# @brief Provede součet dvou čísel
# @param a První číslo
# @param b Druhé číslo
# @return Součet a a b
def add(a,b):
    return a + b



##
# @brief Provede odčítání dvou čísel
# @param a První číslo
# @param b Druhé číslo
# @return Rozdíl a a b
def subtract(a,b):
    return a - b



##
# @brief Provede násobení dvou čísel
# @param a První číslo
# @param b Druhé číslo
# @return Součin a a b
def multiply(a,b):
    return a * b



##
# @brief Provede dělení dvou čísel
# @param a První číslo
# @param b Druhé číslo
# @return Podíl a a b
def divide(a,b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b



##
# @brief Provede umocnění čísla a na b
# @param a Základ
# @param b Mocnitel
# @return Výsledek umocnění
def power(a,b):
    if a == 0 and b < 0:
        raise ValueError("Cannot raise zero to a negative power")
    return a ** b



##
# @brief Provede výpočet n-té odmocniny čísla a
# @param a Číslo, ze kterého se odmocnina počítá
# @param b Stupeň odmocniny
# @return Výsledek odmocniny
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



##
# @brief Provede výpočet faktoriálu čísla n
# @param n Číslo, pro které se faktoriál počítá 
# @return Výsledek faktoriálu
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



##
# @brief Provede výpočet absolutní hodnoty čísla x
# @param x Číslo, pro které se absolutní hodnota počítá
# @return Výsledek absolutní hodnoty
def absolute_value(x):
    return abs(x)



##
# @brief Vyhodnotí matematický výraz zadaný jako řetězec
# @param expression Matematický výraz jako řetězec
# @return Výsledek vyhodnocení výrazu
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
