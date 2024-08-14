# module_2.py


# Long function with nested loops and poor readability
def complex_function(data):
    result = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] > 10:
                for k in range(5):
                    result.append(data[i][j] * k)
            else:
                result.append(data[i][j])
    return result


# Function with improper exception handling
def exception_handling():
    try:
        print(1 / 0)
    except:
        pass  # Catching general exception is a bad practice


# Redundant comments
def add_numbers(a, b):
    # This function adds two numbers
    return a + b


# Function with a potential resource leak
def read_file(file_path):
    file = open(file_path, "r")
    content = file.read()
    # Missing file.close()
    return content


# Function with an unused loop
def unused_loop():
    for i in range(10):
        pass


# Function with a hard-coded path (maintainability issue)
def read_config():
    with open("/etc/config.cfg", "r") as config_file:
        return config_file.read()


# Class with no methods (useless class)
class UselessClass:
    pass


# Complex if-else structure
def complex_decision(x):
    if x > 0:
        if x > 10:
            if x > 20:
                return "x > 20"
            else:
                return "10 < x <= 20"
        else:
            return "0 < x <= 10"
    else:
        return "x <= 0"
