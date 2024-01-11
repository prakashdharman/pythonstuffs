# use_example_class.py
from example_class import Calculator

# Create an instance of the Calculator class
calculator_instance = Calculator()

# Use the methods of the Calculator class
calculator_instance.add(5, 3)
print("Result after addition:", calculator_instance.get_result())

calculator_instance.subtract(7, 2)
print("Result after subtraction:", calculator_instance.get_result())
