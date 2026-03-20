import calc 



# Testy na sčítaní 
def test_calc_add():
    assert calc.add(2, 3) == 5
    assert calc.add(-1, -2) == -3
    assert calc.add(2, -3) == -1
    assert calc.add(-2, 3) == 1
    assert calc.add(0, 0) == 0
    assert calc.add(0, 2) == 2
    assert calc.add(2, 0) == 2
    assert calc.add(-2, 0) == -2
    assert calc.add(0, -2) == -2
    assert calc.add(2.5, 3.5) == 6.0

 # Testy na odčítaní 
def test_calc_subtract():
    assert calc.subtract(5, 2) == 3
    assert calc.subtract(1, 2) == -1
    assert calc.subtract(2, -3) == 5
    assert calc.subtract(-2, 3) == -5
    assert calc.subtract(-3, -2) == -1
    assert calc.subtract(0, 2) == -2
    assert calc.subtract(2, 0) == 2
    assert calc.subtract(0, -2) == 2
    assert calc.subtract(-2, 0) == -2
    assert calc.subtract(0, 0) == 0

# Testy na násobení 
def test_calc_multiply():
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(3, 2) == 6
    assert calc.multiply(-2, 3) == -6
    assert calc.multiply(2, -3) == -6
    assert calc.multiply(-2, -3) == 6
    assert calc.multiply(0, 5) == 0
    assert calc.multiply(5, 0) == 0

# Testy na dělení 
def test_calc_divide():
    assert calc.divide(10, 2) == 5
    assert calc.divide(10, -2) == -5
    assert calc.divide(-10, 2) == -5
    assert calc.divide(-10, -2) == 5
    assert calc.divide(0, 5) == 0
    assert calc.divide(10, 0) == "Error: Division by zero"

 # Testy na mocniny 
def test_calc_power():
    assert calc.power(2, 3) == 8
    assert calc.power(3, 2) == 9
    assert calc.power(-2, 2) == 4
    assert calc.power(-2, 3) == -8
    assert calc.power(2, -1) == 0.5
    assert calc.power(2, 0) == 1
    assert calc.power(0, 2) == 0

 # Testy na odmocniny 
def test_calc_sqrt():
    assert calc.sqrt(16, 2) == 4
    assert calc.sqrt(16, 4) == 2
    assert calc.sqrt(16, 1) == 16
    assert calc.sqrt(16, 3) == 2.5198420997897464
    assert calc.sqrt(16, -2) == "Error: Root degree must be greater than zero"
    assert calc.sqrt(16, 0) == "Error: Root degree must be greater than zero"
    assert calc.sqrt(-16, 2) == "Error: Cannot calculate square root of negative number"
    assert calc.sqrt(0, 2) == 0

 # Testy na faktoriál 
def test_calc_factorial():
    assert calc.factorial(1) == 1
    assert calc.factorial(2) == 2
    assert calc.factorial(3) == 6
    assert calc.factorial(4) == 24
    assert calc.factorial(5) == 120
    assert calc.factorial(0) == 1
    assert calc.factorial(-1) == "Error: Factorial is not defined for negative numbers"
    assert calc.factorial(2.2) == "Error: Factorial is not defined for non-integer numbers"

# Testy na absolutní hodnotu
def test_calc_absolute_value():
    assert calc.absolute_value(5) == 5
    assert calc.absolute_value(-5) == 5
    assert calc.absolute_value(0) == 0
    assert calc.absolute_value(2.5) == 2.5
    assert calc.absolute_value(-2.5) == 2.5
