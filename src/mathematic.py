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
        raise ZeroDivisionError("Nemůžete dělit nulou")
    return a / b



##
# @brief Provede umocnění čísla a na b
# @param a Základ
# @param b Mocnitel
# @return Výsledek umocnění
def power(a,b):
    if a == 0 and b < 0:
        raise ValueError("Nula nemůže být umocněna na zápornou hodnotu")
    if a == 0 and b == 0:
        return 1
    if a < 0 and isinstance(b, float) and not b.is_integer():
        raise ValueError("Komplexní čísla nejsou podporována")
    return a ** b

##
# @brief Provede výpočet druhé odmocniny
# @param a Číslo, ze kterého se odmocnina počítá
# @return Výsledek druhé odmocniny
def sqrt(a):
    if a < 0:
        raise ValueError("Druhá odmocnina není definována pro záporná čísla")
    return a ** 0.5


##
# @brief Provede výpočet n-té odmocniny čísla a
# @param a Číslo, ze kterého se odmocnina počítá
# @param b Stupeň odmocniny
# @return Výsledek odmocniny
def root(a, b):
   # Základní kontroly chyb
    if b == 0:
        raise ValueError("Stupeň odmocniny nemůže být nula")
    # Kontrola pro záporné a reálné b, které by vedly k nedefinovaným výsledkům
    if a < 0 and isinstance(b, float):
        raise ValueError("Komplexní čísla nejsou podporována")
    # Kontrola pro 0 a záporné b, které by vedly k nedefinovaným výsledkům    
    if a == 0 and b < 0:
        raise ValueError("Nula nemůže být umocněna na zápornou hodnotu")
    # Kontrola pro záporné a sudé b, které by vedly k nedefinovaným výsledkům   
    if a < 0 and b % 2 == 0:
        raise ValueError("Druhá odmocnina není definována pro záporná čísla")
    # Výpočet pro záporné b 
    if b < 0:
        res = abs(a) ** (1 / abs(b))
        return -res if (a < 0 or b < 0) else res
    # Výpočet lichých odmocnin ze záporných čísel
    if a < 0:
        return -((-a) ** (1 / b))
    # Standardní výpočet
    return a ** (1 / b)



##
# @brief Provede výpočet faktoriálu čísla n
# @param n Číslo, pro které se faktoriál počítá 
# @return Výsledek faktoriálu
def factorial(n):
    # Kontrola vstupních hodnot
    if not isinstance(n, int):
        raise ValueError("Faktoriál není definován pro necelá čísla")
    # Kontrola pro záporné čísla 
    if n < 0:
        raise ValueError("Faktoriál není definován pro záporná čísla")
    # Kontrola pro příliš velké číslo, které by mohlo způsobit přetečení
    if n > 170:
        raise ValueError("Výsledek faktoriálu je příliš velký na zvládnutí")
    # Výpočet faktoriálu pro n = 0 a n = 1
    elif n == 0 or n == 1:
        return 1
    # Výpočet faktoriálu pro n > 1
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
    #Definujeme povolené funkce pro eval
    allowed_names = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'power': power,
        'root': root,
        'factorial': factorial,
        'absolute_value': absolute_value,
        'sqrt': sqrt,
    }
    # Vyhodnotíme výraz s omezením na povolené funkce
    return eval(expression, {"__builtins__": {}}, allowed_names)
