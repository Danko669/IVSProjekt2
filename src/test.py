import calc 
import math

###########################
# Testy add 

###########################

# Testy na přidání kladných čísel
def test_calc_add_positive():
    assert calc.add(2, 3) == 5
    assert calc.add(2.5, 3.5) == 6.0

# Testy na přidání záporných čísel
def test_calc_add_negative():
    assert calc.add(-2, -3) == -5
    assert calc.add(-4, -2) == -6
    assert calc.add(-2.5, -3.5) == -6.0

# Testy na přidání smíšených čísel
def test_calc_add_mixed():
    assert calc.add(2, -3) == -1
    assert calc.add(-2, 3) == 1
    assert calc.add(2.5, -3.5) == -1.0
    assert calc.add(-2.5, 3.5) == 1.0

# Testy na přidání nuly    
def test_calc_add_zero():
    assert calc.add(0, 0) == 0
    assert calc.add(0, 5) == 5
    assert calc.add(5, 0) == 5
    assert calc.add(0, -5) == -5
    assert calc.add(-5, 0) == -5
    assert calc.add(2.5, 0) == 2.5
    assert calc.add(0, 2.5) == 2.5




###########################   
 
 # Testy na odčítaní 

###########################

# Testy na odčítaní kladných čísel
def test_calc_subtract_positive():
    assert calc.subtract(5, 2) == 3
    assert calc.subtract(2, 5) == -3
    assert calc.subtract(5.5, 2.5) == 3.0
    assert calc.subtract(2.5, 5.5) == -3.0

# Testy na odčítaní záporných čísel
def test_calc_subtract_negative():
    assert calc.subtract(-5, -2) == -3
    assert calc.subtract(-2, -5) == 3
    assert calc.subtract(-5.5, -2.5) == -3.0
    assert calc.subtract(-2.5, -5.5) == 3.0

# Testy na odčítaní smíšených čísel
def test_calc_subtract_mixed():
    assert calc.subtract(2, -3) == 5
    assert calc.subtract(-2, 3) == -5
    assert calc.subtract(2.5, -3.5) == 6.0
    assert calc.subtract(-2.5, 3.5) == -6.0

# Testy na odčítaní nuly
def test_calc_subtract_zero():
    assert calc.subtract(0, 0) == 0
    assert calc.subtract(0, 5) == -5
    assert calc.subtract(5, 0) == 5
    assert calc.subtract(0, -5) == 5
    assert calc.subtract(-5, 0) == -5
    assert calc.subtract(0, 2.5) == -2.5
    assert calc.subtract(2.5, 0) == 2.5



###########################
# Testy na násobení 

###########################

# Testy na násobení kladných čísel
def test_calc_multiply_positive():
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(3, 2) == 6
    assert calc.multiply(2.5, 3.5) == 8.75
    assert calc.multiply(3.5, 2.5) == 8.75

# Testy na násobení záporných čísel
def test_calc_multiply_negative():
    assert calc.multiply(-2, -3) == 6
    assert calc.multiply(-3, -2) == 6
    assert calc.multiply(-2.5, -3.5) == 8.75
    assert calc.multiply(-3.5, -2.5) == 8.75
   
# Testy na násobení smíšených čísel
def test_calc_multiply_mixed():
    assert calc.multiply(2, -3) == -6
    assert calc.multiply(-2, 3) == -6
    assert calc.multiply(2.5, -3.5) == -8.75
    assert calc.multiply(-2.5, 3.5) == -8.75

# Testy na násobení nuly
def test_calc_multiply_zero():
    assert calc.multiply(0, 0) == 0
    assert calc.multiply(0, 5) == 0
    assert calc.multiply(5, 0) == 0
    assert calc.multiply(0, -5) == 0
    assert calc.multiply(-5, 0) == 0
    assert calc.multiply(0, 2.5) == 0
    assert calc.multiply(2.5, 0) == 0




###########################
# Testy na dělení 

###########################

# Testy na dělení kladných čísel
def test_calc_divide_positive():
    assert calc.divide(10, 2) == 5
    assert calc.divide(10, 5) == 2
    assert calc.divide(2, 10) == 0.2
    assert calc.divide(5.5, 2.5) == 2.2
    assert math.isclose(calc.divide(2.5, 5.5), 0.45454545454545453)

# Testy na dělení záporných čísel
def test_calc_divide_negative():
    assert calc.divide(-10, -2) == 5
    assert calc.divide(-10, -5) == 2
    assert calc.divide(-2, -10) == 0.2
    assert calc.divide(-5.5, -2.5) == 2.2
    assert math.isclose(calc.divide(-2.5, -5.5), 0.45454545454545453)

# Testy na dělení smíšených čísel
def test_calc_divide_mixed():
    assert calc.divide(10, -2) == -5
    assert calc.divide(-10, 2) == -5
    assert calc.divide(2, -10) == -0.2
    assert calc.divide(-5.5, 2.5) == -2.2
    assert math.isclose(calc.divide(2.5, -5.5), -0.45454545454545453)


# Testy na dělení nuly
def test_calc_divide_zero():
    assert calc.divide(0, 5) == 0
    assert calc.divide(0, -5) == 0
    assert calc.divide(0, 0) == "Error: Division by zero"
    assert calc.divide(5, 0) == "Error: Division by zero"
    assert calc.divide(-5, 0) == "Error: Division by zero"
    assert calc.divide(0, 2.5) == 0
    assert calc.divide(0, -2.5) == 0
    assert calc.divide(2.5, 0) == "Error: Division by zero"
    assert calc.divide(-2.5, 0) == "Error: Division by zero"


###########################
 # Testy na mocniny 

###########################

# Testy na mocniny kladných čísel
def test_calc_power_positive():
    assert calc.power(2, 3) == 8
    assert calc.power(2, 2) == 4
    assert calc.power(2, 1) == 2
    assert calc.power(2.5, 1) == 2.5
    assert calc.power(2.5, 2) == 6.25
    assert calc.power(2, 2.5) == "Error: Complex numbers are not supported"

# Testy na mocniny záporných čísel
def test_calc_power_negative():
    assert calc.power(-2, -1) == -0.5
    assert calc.power(-2, -2) == 0.25
    assert calc.power(-2.5, -3) == -0.064
    assert calc.power(-2.5, -2) == 0.16
    assert calc.power(-2, 2.5) == "Error: Complex numbers are not supported"

# Testy na mocniny smíšených čísel
def test_calc_power_mixed():
    assert calc.power(-2, 3) == -8
    assert calc.power(-2, 2) == 4
    assert calc.power(2, -1) == 0.5
    assert calc.power(2, -2) == 0.25
    assert calc.power(2.5, -2) == 0.16
    assert calc.power(-2.5, 2) == 6.25
    assert calc.power(-2, 2.5) == "Error: Complex numbers are not supported"
    assert calc.power(2, -2.5) == "Error: Complex numbers are not supported"

# Testy na mocniny nuly
def test_calc_power_zero():
    assert calc.power(0, 0) == "Error: Zero cannot be raised to the power of zero"
    assert calc.power(0, 2) == 0
    assert calc.power(0, -2) == "Error: Zero cannot be raised to a negative power"
    assert calc.power(2, 0) == 1
    assert calc.power(-2, 0) == 1
    assert calc.power(0, 2.5) == 0
    assert calc.power(0, -2.5) == "Error: Zero cannot be raised to a negative power"
    assert calc.power(2.5, 0) == 1
    assert calc.power(-2.5, 0) == 1




###########################
# Testy na odmocniny 

###########################

# Testy na odmocniny kladných čísel
def test_calc_sqrt_positive():
    assert calc.sqrt(4, 2) == 2
    assert calc.sqrt(9, 2) == 3
    assert calc.sqrt(27, 3) == 3
    assert calc.sqrt(16, 4) == 2
    assert calc.sqrt(2.25, 2) == 1.5
    assert calc.sqrt(1, 3) == 1
    assert calc.sqrt(1, 2) == 1
    assert calc.sqrt(2, 2.5) == "Error: Complex numbers are not supported"

# Testy na odmocniny záporných čísel
def test_calc_sqrt_negative():
    assert calc.sqrt(-2, -2) == "Error: Square root is not defined for negative numbers"
    assert calc.sqrt(-8, -3) == "Error: Cube root is not defined for negative numbers"
    assert calc.sqrt(-16, -4) == "Error: Fourth root is not defined for negative numbers"
    assert calc.sqrt(-2.25, -2) == "Error: Square root is not defined for negative numbers"
    assert calc.sqrt(-1, -3) == "Error: Cube root is not defined for negative numbers"

# Testy na odmocniny smíšených čísel
def test_calc_sqrt_mixed():
    assert calc.sqrt(2, -2) == "Error: Square root is not defined for negative numbers"
    assert calc.sqrt(-2, 2) == "Error: Square root is not defined for negative numbers"
    assert calc.sqrt(8, -3) == "Error: Cube root is not defined for negative numbers"
    assert calc.sqrt(-8, 3) == "Error: Cube root is not defined for negative numbers"
    assert calc.sqrt(2.25, -2) == "Error: Square root is not defined for negative numbers"
    assert calc.sqrt(-2.25, 2) == "Error: Square root is not defined for negative numbers"
    assert calc.sqrt(-2, 2.5) == "Error: Complex numbers are not supported"

# Testy na odmocniny nuly
def test_calc_sqrt_zero():
    assert calc.sqrt(0, 2) == 0
    assert calc.sqrt(0, 3) == 0
    assert calc.sqrt(0, 4) == 0
    assert calc.sqrt(0, 2.5) == "Error: Complex numbers are not supported"
    assert calc.sqrt(0, -2) == "Error: 0 cannot be raised to a negative power"
    assert calc.sqrt(0, -3) == "Error: 0 cannot be raised to a negative power"
    assert calc.sqrt(1, 0) == "Error: Root degree cannot be zero"
    assert calc.sqrt(5, 0) == "Error: Root degree cannot be zero"
    assert calc.sqrt(0, 0) == "Error: Root degree cannot be zero"
    assert calc.sqrt(2.5, 0) == "Error: Root degree cannot be zero"
     
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
    assert calc.factorial(2.2) == "Error: Factorial is not defined for non-integer numbers"

# Testy na faktoriál záporných čísel
def test_calc_factorial_negative():
    assert calc.factorial(-3) == "Error: Factorial is not defined for negative numbers" 
    assert calc.factorial(-1) == "Error: Factorial is not defined for negative numbers"
    assert calc.factorial(-2.5) == "Error: Factorial is not defined for negative numbers"  

# Testy na faktoriál nuly
def test_calc_factorial_zero():
    assert calc.factorial(0) == 1
   

###########################
# Testy na absolutní hodnotu

###########################
def test_calc_absolute_value():
    assert calc.absolute_value(5) == 5
    assert calc.absolute_value(-5) == 5
    assert calc.absolute_value(0) == 0
    assert calc.absolute_value(2.5) == 2.5
    assert calc.absolute_value(-2.5) == 2.5
