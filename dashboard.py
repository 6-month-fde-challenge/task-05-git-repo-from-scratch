"""Final integration point for the project.

Imports the four results already computed by calculator.py and prints them as a
single report. Run this file to exercise every other module in one go:

    python dashboard.py
"""

from calculator import total, subtraction, multiplication, div

print("*********** CALCULATOR DASHBOARD ***********")
print("Result of addition is       : ", total)
print("Result of subtraction is    : ", subtraction)
print("Result of multiplication is : ", multiplication)
print("Result of division is       : ", div)
print("********************************************")
