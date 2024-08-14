# module_1.py

# Unused import

# Unused variable
x = 10

# Hard-coded credentials
username = "admin"
password = "password123"


# Function with too many arguments (code smell)
def process_data(a, b, c, d, e, f, g):
    return a + b + c + d + e + f + g


# Function with duplicated code
def duplicated_function():
    print("This is duplicated code.")
    print("This is duplicated code.")


# Security issue: using eval
def insecure_eval(input_string):
    eval(input_string)


# Bug: Division by zero
def divide_numbers(a, b):
    return a / b


# Empty function
def empty_function():
    pass


# Function with unused arguments
def function_with_unused_args(a, b, c):
    return a + b


# Function that always returns the same value (dead code)
def always_returns_same():
    return 42
