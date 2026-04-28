##
# @file profiling.py
# @brief Skript pro výpočet směrodatné odchylky z dat
# @author Václav Král xkralva00
# @date 2026-04-20


import sys
import mathematic as mat

##
# @brief Hlavní funkce pro výpočet směrodatné odchylky
# @detail Skript načítá čísla ze standardního vstupu, vypočítá průměr, rozptyl a nakonec směrodatnou odchylku. Výsledek je vypsán na standardní výstup.
# @return Výsledek výpočtu směrodatné odchylky

## Načtení dat ze standardního vstupu
number =[float(x) for x in sys.stdin.read().split()]
length = len(number)
if length < 2:
    print("Minimální počet čísel pro výpočet směrodatné odchylky je 2.")
    sys.exit(1)

# @brief Výpočet průměru
# @param number Seznam načtených čísel
# @param length Počet načtených čísel
# @return Průměr dat
total = 0
for x in number:
    total = mat.add(total, x)
mean = mat.divide(total, length)


# @brief Výpočet rozptylu
# @param number Seznam načtených čísel
# @param mean Průměr dat
# @param length Počet načtených čísel
# @return Rozptyl dat
variance_total = 0
for x in number:
    variance_total = mat.add(variance_total, mat.power(mat.subtract(x, mean), 2))
variance = mat.divide(variance_total, mat.subtract(length, 1))


# @brief Výpočet směrodatné odchylky
# @param variance Rozptyl dat
# @return Výsledek výpočtu směrodatné odchylky
std_dev = mat.root(variance, 2) 
print(f"Standard Deviation: {std_dev}")
