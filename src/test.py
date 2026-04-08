import calc 
import math
import pytest

###########################
# Testy add 

###########################

# Testy na přidání kladných čísel
def test_calc_add_positive():
    assert calc.add(2, 3) == 5
    assert math.isclose(calc.add(2.5, 3.5), 6.0)

# Testy na přidání záporných čísel
def test_calc_add_negative():
    assert calc.add(-2, -3) == -5
    assert calc.add(-4, -2) == -6
    assert math.isclose(calc.add(-2.5, -3.5), -6.0)

# Testy na přidání smíšených čísel
def test_calc_add_mixed():
    assert calc.add(2, -3) == -1
    assert calc.add(-2, 3) == 1
    assert math.isclose(calc.add(2.5, -3.5), -1.0)
    assert math.isclose(calc.add(-2.5, 3.5), 1.0)

# Testy na přidání nuly    
def test_calc_add_zero():
    assert calc.add(0, 0) == 0
    assert calc.add(0, 5) == 5
    assert calc.add(5, 0) == 5
    assert calc.add(0, -5) == -5
    assert calc.add(-5, 0) == -5
    assert math.isclose(calc.add(2.5, 0), 2.5)
    assert math.isclose(calc.add(0, 2.5), 2.5)




###########################   
 
 # Testy na odčítaní 

###########################

# Testy na odčítaní kladných čísel
def test_calc_subtract_positive():
    assert calc.subtract(5, 2) == 3
    assert calc.subtract(2, 5) == -3
    assert math.isclose(calc.subtract(5.5, 2.5), 3.0)
    assert math.isclose(calc.subtract(2.5, 5.5), -3.0)

# Testy na odčítaní záporných čísel
def test_calc_subtract_negative():
    assert calc.subtract(-5, -2) == -3
    assert calc.subtract(-2, -5) == 3
    assert math.isclose(calc.subtract(-5.5, -2.5), -3.0)
    assert math.isclose(calc.subtract(-2.5, -5.5), 3.0)

# Testy na odčítaní smíšených čísel
def test_calc_subtract_mixed():
    assert calc.subtract(2, -3) == 5
    assert calc.subtract(-2, 3) == -5
    assert math.isclose(calc.subtract(2.5, -3.5), 6.0)
    assert math.isclose(calc.subtract(-2.5, 3.5), -6.0)

# Testy na odčítaní nuly
def test_calc_subtract_zero():
    assert calc.subtract(0, 0) == 0
    assert calc.subtract(0, 5) == -5
    assert calc.subtract(5, 0) == 5
    assert calc.subtract(0, -5) == 5
    assert calc.subtract(-5, 0) == -5
    assert math.isclose(calc.subtract(0, 2.5), -2.5)
    assert math.isclose(calc.subtract(2.5, 0), 2.5)



###########################
# Testy na násobení 

###########################

# Testy na násobení kladných čísel
def test_calc_multiply_positive():
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(3, 2) == 6
    assert math.isclose(calc.multiply(2.5, 3.5), 8.75)
    assert math.isclose(calc.multiply(3.5, 2.5), 8.75)

# Testy na násobení záporných čísel
def test_calc_multiply_negative():
    assert calc.multiply(-2, -3) == 6
    assert calc.multiply(-3, -2) == 6
    assert math.isclose(calc.multiply(-2.5, -3.5), 8.75)
    assert math.isclose(calc.multiply(-3.5, -2.5), 8.75)

# Testy na násobení smíšených čísel
def test_calc_multiply_mixed():
    assert calc.multiply(2, -3) == -6
    assert calc.multiply(-2, 3) == -6
    assert math.isclose(calc.multiply(2.5, -3.5), -8.75)
    assert math.isclose(calc.multiply(-2.5, 3.5), -8.75)

# Testy na násobení nuly
def test_calc_multiply_zero():
    assert calc.multiply(0, 0) == 0
    assert calc.multiply(0, 5) == 0
    assert calc.multiply(5, 0) == 0
    assert calc.multiply(0, -5) == 0
    assert calc.multiply(-5, 0) == 0
    assert math.isclose(calc.multiply(0, 2.5), 0)
    assert math.isclose(calc.multiply(2.5, 0), 0)




###########################
# Testy na dělení 

###########################

# Testy na dělení kladných čísel
def test_calc_divide_positive():
    assert calc.divide(10, 2) == 5
    assert calc.divide(10, 5) == 2
    assert calc.divide(2, 10) == 0.2
    assert math.isclose(calc.divide(5.5, 2.5), 2.2)
    assert math.isclose(calc.divide(2.5, 5.5), 0.45454545454545453)

# Testy na dělení záporných čísel
def test_calc_divide_negative():
    assert calc.divide(-10, -2) == 5
    assert calc.divide(-10, -5) == 2
    assert calc.divide(-2, -10) == 0.2
    assert math.isclose(calc.divide(-5.5, -2.5), 2.2)
    assert math.isclose(calc.divide(-2.5, -5.5), 0.45454545454545453)

# Testy na dělení smíšených čísel
def test_calc_divide_mixed():
    assert calc.divide(10, -2) == -5
    assert calc.divide(-10, 2) == -5
    assert calc.divide(2, -10) == -0.2
    assert math.isclose(calc.divide(-5.5, 2.5), -2.2)
    assert math.isclose(calc.divide(2.5, -5.5), -0.45454545454545453)


# Testy na dělení nuly
def test_calc_divide_zero():
    assert calc.divide(0, 5) == 0
    assert calc.divide(0, -5) == 0
    assert calc.divide(0, 2.5) == 0
    assert calc.divide(0, -2.5) == 0

# Testy na chyby při dělení
def test_divide_errors():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(5, 0)
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(-5, 0)
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(2.5, 0)
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(-2.5, 0) 


###########################
 # Testy na mocniny 

###########################

# Testy na mocniny kladných čísel
def test_calc_power_positive():
    assert calc.power(2, 3) == 8
    assert calc.power(2, 2) == 4
    assert calc.power(2, 1) == 2
    assert math.isclose(calc.power(2.5, 1), 2.5)
    assert math.isclose(calc.power(2.5, 2), 6.25)

# Testy na mocniny záporných čísel
def test_calc_power_negative():
    assert calc.power(-2, -1) == -0.5
    assert calc.power(-2, -2) == 0.25
    assert math.isclose(calc.power(-2.5, -3), -0.064)
    assert math.isclose(calc.power(-2.5, -2), 0.16)

# Testy na mocniny smíšených čísel
def test_calc_power_mixed():
    assert calc.power(-2, 3) == -8
    assert calc.power(-2, 2) == 4
    assert calc.power(2, -1) == 0.5
    assert calc.power(2, -2) == 0.25
    assert math.isclose(calc.power(2.5, -2), 0.16)
    assert math.isclose(calc.power(-2.5, 2), 6.25)
    assert math.isclose(calc.power(2, -2.5), 0.16)

# Testy na mocniny nuly
def test_calc_power_zero():
    assert calc.power(0, 2) == 0
    assert calc.power(2, 0) == 1
    assert calc.power(-2, 0) == 1
    assert math.isclose(calc.power(0, 2.5), 0)
    assert math.isclose(calc.power(2.5, 0), 1)
    assert math.isclose(calc.power(-2.5, 0), 1)

# Testy na chyby při výpočtu mocnin
def test_power_errors():
    with pytest.raises(ValueError, match="Zero cannot be raised to the power of zero"):
        calc.power(0, 0)
    with pytest.raises(ValueError, match="Zero cannot be raised to a negative power"):
        calc.power(0, -2)
    with pytest.raises(ValueError, match="Complex numbers are not supported"):
        calc.power(-2, 2.5)



###########################
# Testy na odmocniny 

###########################

# Testy na odmocniny kladných čísel
def test_calc_root_positive():
    assert calc.root(4, 2) == 2
    assert calc.root(9, 2) == 3
    assert calc.root(27, 3) == 3
    assert calc.root(16, 4) == 2
    assert math.isclose(calc.root(2.25, 2), 1.5)
    assert calc.root(1, 3) == 1
    assert calc.root(1, 2) == 1

# Testy na odmocniny záporných čísel
def test_calc_root_negative():
    assert math.isclose(calc.root(-8, -3), -2)
    assert math.isclose(calc.root(-1, -3), -1)

# Testy na odmocniny smíšených čísel
def test_calc_root_mixed():
    assert math.isclose(calc.root(8, -3), -2)
    assert math.isclose(calc.root(-8, 3), -2)

# Testy na odmocniny nuly
def test_calc_root_zero():
    assert calc.root(0, 2) == 0
    assert calc.root(0, 3) == 0
    assert calc.root(0, 4) == 0

# Testy na chyby při výpočtu odmocnin
def test_root_errors():
    with pytest.raises(ValueError, match="Root degree cannot be zero"):
        calc.root(5, 0)
    with pytest.raises(ValueError, match="0 cannot be raised to a negative power"):
        calc.root(0, -2)
    with pytest.raises(ValueError, match="Square root is not defined for negative numbers"):
        calc.root(-4, 2)
    with pytest.raises(ValueError, match="Complex numbers are not supported"):
        calc.root(-2, 2.5)   
     
###########################
 # Testy na faktoriál 

 ###########################

# Testy na faktoriál kladných čísel
def test_calc_factorial_positive():
    assert calc.factorial(1) == 1
    assert calc.factorial(2) == 2
    assert calc.factorial(3) == 6
    assert calc.factorial(4) == 24
    assert calc.factorial(5) == 120
 

# Testy na faktoriál nuly
def test_calc_factorial_zero():
    assert calc.factorial(0) == 1

# Testy na chyby při výpočtu faktoriálu
def test_factorial_errors():
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        calc.factorial(-1)
    with pytest.raises(ValueError, match="Factorial is not defined for non-integer numbers"):
        calc.factorial(2.5)
   

###########################
# Testy na absolutní hodnotu

###########################
def test_calc_absolute_value():
    assert calc.absolute_value(5) == 5
    assert calc.absolute_value(-5) == 5
    assert calc.absolute_value(0) == 0
    assert calc.absolute_value(2.5) == 2.5
    assert calc.absolute_value(-2.5) == 2.5


###########################
# Testy na vyhodnocení matematického výrazu

###########################
def test_calc_evaluate():
    assert calc.evaluate("add(2, multiply(3, 4))") == 14
    assert calc.evaluate("power(2, 3) + factorial(3)") == 14
    assert calc.evaluate("root(16,2) + absolute_value(-4)") == 8
    assert calc.evaluate("subtract(10, divide(20, 4))") == 5
    assert calc.evaluate("factorial(5) - power(2, 3)") == 112
    assert calc.evaluate("absolute_value(-3) + root(27, 3)") == 6
    assert calc.evaluate("add(2.5, multiply(3.5, 4))") == 16.5
    assert calc.evaluate("power(2.5, 3) + factorial(4)") == 30.625
    assert calc.evaluate("root(2.25, 2) + absolute_value(-1.5)") == 3.0
    with pytest.raises(NameError):
        calc.evaluate("invalid_function(2, 3)")
