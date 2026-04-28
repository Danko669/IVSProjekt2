##
# @file test.py
# @brief TDD testy pro matematickou knihovnu
# @author Václav Král xkralva00
# @date 2026-04-02


import mathematic as mat
import math
import pytest


##
# @brief Testy pro funkci add kladných čísel
def test_mat_add_positive():
    assert mat.add(2, 3) == 5
    assert math.isclose(mat.add(2.5, 3.5), 6.0)

##
# @brief Testy pro funkci add záporných čísel
def test_mat_add_negative():
    assert mat.add(-2, -3) == -5
    assert mat.add(-4, -2) == -6
    assert math.isclose(mat.add(-2.5, -3.5), -6.0)

##
# @brief Testy pro funkci add smíšených čísel
def test_mat_add_mixed():
    assert mat.add(2, -3) == -1
    assert mat.add(-2, 3) == 1
    assert math.isclose(mat.add(2.5, -3.5), -1.0)
    assert math.isclose(mat.add(-2.5, 3.5), 1.0)

##
# @brief Testy pro funkci add nuly
def test_mat_add_zero():
    assert mat.add(0, 0) == 0
    assert mat.add(0, 5) == 5
    assert mat.add(5, 0) == 5
    assert mat.add(0, -5) == -5
    assert mat.add(-5, 0) == -5
    assert math.isclose(mat.add(2.5, 0), 2.5)
    assert math.isclose(mat.add(0, 2.5), 2.5)




##
# @brief Testy pro funkci subtract kladných čísel
def test_mat_subtract_positive():
    assert mat.subtract(5, 2) == 3
    assert mat.subtract(2, 5) == -3
    assert math.isclose(mat.subtract(5.5, 2.5), 3.0)
    assert math.isclose(mat.subtract(2.5, 5.5), -3.0)

##
# @brief Testy pro funkci subtract záporných čísel
def test_mat_subtract_negative():
    assert mat.subtract(-5, -2) == -3
    assert mat.subtract(-2, -5) == 3
    assert math.isclose(mat.subtract(-5.5, -2.5), -3.0)
    assert math.isclose(mat.subtract(-2.5, -5.5), 3.0)

##
# @brief Testy pro funkci subtract smíšených čísel
def test_mat_subtract_mixed():
    assert mat.subtract(2, -3) == 5
    assert mat.subtract(-2, 3) == -5
    assert math.isclose(mat.subtract(2.5, -3.5), 6.0)
    assert math.isclose(mat.subtract(-2.5, 3.5), -6.0)

##
# @brief Testy pro funkci subtract nuly
def test_mat_subtract_zero():
    assert mat.subtract(0, 0) == 0
    assert mat.subtract(0, 5) == -5
    assert mat.subtract(5, 0) == 5
    assert mat.subtract(0, -5) == 5
    assert mat.subtract(-5, 0) == -5
    assert math.isclose(mat.subtract(0, 2.5), -2.5)
    assert math.isclose(mat.subtract(2.5, 0), 2.5)




##
# @brief Testy pro funkci multiply kladných čísel
def test_mat_multiply_positive():
    assert mat.multiply(2, 3) == 6
    assert mat.multiply(3, 2) == 6
    assert math.isclose(mat.multiply(2.5, 3.5), 8.75)
    assert math.isclose(mat.multiply(3.5, 2.5), 8.75)

##
# @brief Testy pro funkci multiply záporných čísel
def test_mat_multiply_negative():
    assert mat.multiply(-2, -3) == 6
    assert mat.multiply(-3, -2) == 6
    assert math.isclose(mat.multiply(-2.5, -3.5), 8.75)
    assert math.isclose(mat.multiply(-3.5, -2.5), 8.75)

##
# @brief Testy pro funkci multiply smíšených čísel
def test_mat_multiply_mixed():
    assert mat.multiply(2, -3) == -6
    assert mat.multiply(-2, 3) == -6
    assert math.isclose(mat.multiply(2.5, -3.5), -8.75)
    assert math.isclose(mat.multiply(-2.5, 3.5), -8.75)

##
# @brief Testy pro funkci multiply nuly
def test_mat_multiply_zero():
    assert mat.multiply(0, 0) == 0
    assert mat.multiply(0, 5) == 0
    assert mat.multiply(5, 0) == 0
    assert mat.multiply(0, -5) == 0
    assert mat.multiply(-5, 0) == 0
    assert math.isclose(mat.multiply(0, 2.5), 0)
    assert math.isclose(mat.multiply(2.5, 0), 0)




##
# @brief Testy pro funkci divide kladných čísel
def test_mat_divide_positive():
    assert mat.divide(10, 2) == 5
    assert mat.divide(10, 5) == 2
    assert mat.divide(2, 10) == 0.2
    assert math.isclose(mat.divide(5.5, 2.5), 2.2)
    assert math.isclose(mat.divide(2.5, 5.5), 0.45454545454545453)

##
# @brief Testy pro funkci divide záporných čísel
def test_mat_divide_negative():
    assert mat.divide(-10, -2) == 5
    assert mat.divide(-10, -5) == 2
    assert mat.divide(-2, -10) == 0.2
    assert math.isclose(mat.divide(-5.5, -2.5), 2.2)
    assert math.isclose(mat.divide(-2.5, -5.5), 0.45454545454545453)

##
# @brief Testy pro funkci divide smíšených čísel
def test_mat_divide_mixed():
    assert mat.divide(10, -2) == -5
    assert mat.divide(-10, 2) == -5
    assert mat.divide(2, -10) == -0.2
    assert math.isclose(mat.divide(-5.5, 2.5), -2.2)
    assert math.isclose(mat.divide(2.5, -5.5), -0.45454545454545453)

##
# Testy pro funkci divide nuly
def test_mat_divide_zero():
    assert mat.divide(0, 5) == 0
    assert mat.divide(0, -5) == 0
    assert mat.divide(0, 2.5) == 0
    assert mat.divide(0, -2.5) == 0

##
# @brief Testy pro funkci divide chyby
def test_mat_divide_errors():
    with pytest.raises(ZeroDivisionError, match="Nemůžete dělit nulou"):
        mat.divide(5, 0)
    with pytest.raises(ZeroDivisionError, match="Nemůžete dělit nulou"):
        mat.divide(-5, 0)
    with pytest.raises(ZeroDivisionError, match="Nemůžete dělit nulou"):
        mat.divide(2.5, 0)
    with pytest.raises(ZeroDivisionError, match="Nemůžete dělit nulou"):
        mat.divide(-2.5, 0) 




##
# @brief Testy pro funkci power kladných čísel
def test_mat_power_positive():
    assert mat.power(2, 3) == 8
    assert mat.power(2, 2) == 4
    assert mat.power(2, 1) == 2
    assert math.isclose(mat.power(2.5, 1), 2.5)
    assert math.isclose(mat.power(2.5, 2), 6.25)

##
# @brief Testy pro funkci power záporných čísel
def test_mat_power_negative():
    assert mat.power(-2, -1) == -0.5
    assert mat.power(-2, -2) == 0.25
    assert math.isclose(mat.power(-2.5, -3), -0.064)
    assert math.isclose(mat.power(-2.5, -2), 0.16)

##
# @brief Testy pro funkci power smíšených čísel
def test_mat_power_mixed():
    assert mat.power(-2, 3) == -8
    assert mat.power(-2, 2) == 4
    assert mat.power(2, -1) == 0.5
    assert mat.power(2, -2) == 0.25
    assert math.isclose(mat.power(2.5, -2), 0.16)
    assert math.isclose(mat.power(-2.5, 2), 6.25)
    assert math.isclose(mat.power(2, -2.5), 0.1767766952966369)

##
# @brief Testy pro funkci power nuly
def test_mat_power_zero():
    assert mat.power(0, 0) == 1
    assert mat.power(0, 2) == 0
    assert mat.power(2, 0) == 1
    assert mat.power(-2, 0) == 1
    assert math.isclose(mat.power(0, 2.5), 0)
    assert math.isclose(mat.power(2.5, 0), 1)
    assert math.isclose(mat.power(-2.5, 0), 1)

##
# @brief Testy pro funkci power chyby
def test_mat_power_errors():
    with pytest.raises(ValueError, match="Nula nemůže být umocněna na zápornou hodnotu"):
        mat.power(0, -2)
    with pytest.raises(ValueError, match="Komplexní čísla nejsou podporována"):
        mat.power(-2, 2.5)




##
# @brief Testy pro funkci root kladných čísel
def test_mat_root_positive():
    assert mat.root(4, 2) == 2
    assert mat.root(9, 2) == 3
    assert mat.root(27, 3) == 3
    assert mat.root(16, 4) == 2
    assert math.isclose(mat.root(2.25, 2), 1.5)
    assert mat.root(1, 3) == 1
    assert mat.root(1, 2) == 1

##
# @brief Testy pro funkci root smíšených čísel
def test_mat_root_mixed():
    assert math.isclose(mat.root(-8, 3), -2)
    assert math.isclose(mat.root(-27, 3), -3)
    assert math.isclose(mat.root(-1, 3), -1)

##
# @brief Testy pro funkci root nuly
def test_mat_root_zero():
    assert mat.root(0, 2) == 0
    assert mat.root(0, 3) == 0
    assert mat.root(0, 4) == 0

##
# @brief Testy pro funkci root chyby
def test_mat_root_errors():
    with pytest.raises(ValueError, match="Druhá odmocnina není definována pro záporná čísla"):
        mat.root(-4, 2)
    with pytest.raises(ValueError, match="Komplexní čísla nejsou podporována"):
        mat.root(-2, 2.5)   
    with pytest.raises(ValueError, match="Odmocnina musí být kladné číslo"):
        mat.root(5, -2)

##
# @brief Testy pro funkci sqrt kladných čísel
def test_mat_sqrt_positive():
    assert mat.sqrt(4) == 2
    assert mat.sqrt(9) == 3
    assert math.isclose(mat.sqrt(2.25), 1.5)

##
# @brief Testy pro funkci sqrt záporných čísel
def test_mat_sqrt_negative():
    with pytest.raises(ValueError, match="Druhá odmocnina není definována pro záporná čísla"):
        mat.sqrt(-1)
    with pytest.raises(ValueError, match="Druhá odmocnina není definována pro záporná čísla"):
        mat.sqrt(-4)

##
# @brief Testy pro funkci sqrt nuly
def test_mat_sqrt_zero():
    assert mat.sqrt(0) == 0

##
# @brief Testy pro funkci factorial kladných čísel
def test_mat_factorial_positive():
    assert mat.factorial(1) == 1
    assert mat.factorial(2) == 2
    assert mat.factorial(3) == 6
    assert mat.factorial(4) == 24
    assert mat.factorial(5) == 120
 
##
# @brief Testy pro funkci factorial nuly
def test_mat_factorial_zero():
    assert mat.factorial(0) == 1

##
# @brief Testy pro funkci factorial chyby
def test_mat_factorial_errors():
    with pytest.raises(ValueError, match="Faktoriál není definován pro záporná čísla"):
        mat.factorial(-1)
    with pytest.raises(ValueError, match="Faktoriál není definován pro necelá čísla"):
        mat.factorial(2.5)
   


##
# @brief Testy pro funkci absolute_value 
def test_mat_absolute_value():
    assert mat.absolute_value(5) == 5
    assert mat.absolute_value(-5) == 5
    assert mat.absolute_value(0) == 0
    assert mat.absolute_value(2.5) == 2.5
    assert mat.absolute_value(-2.5) == 2.5




##
# @brief Testy pro funkci evaluate
def test_mat_evaluate():
    assert mat.evaluate("add(2, multiply(3, 4))") == 14
    assert mat.evaluate("power(2, 3) + factorial(3)") == 14
    assert mat.evaluate("root(16,2) + absolute_value(-4)") == 8
    assert mat.evaluate("subtract(10, divide(20, 4))") == 5
    assert mat.evaluate("factorial(5) - power(2, 3)") == 112
    assert mat.evaluate("absolute_value(-3) + root(27, 3)") == 6
    assert mat.evaluate("add(2.5, multiply(3.5, 4))") == 16.5
    assert mat.evaluate("power(2.5, 3) + factorial(4)") == 39.625
    assert mat.evaluate("root(2.25, 2) + absolute_value(-1.5)") == 3.0
    with pytest.raises(NameError):
        mat.evaluate("invalid_function(2, 3)")
