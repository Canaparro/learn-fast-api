# test_module_2.py
from src.sonarissues.module2 import (
    add_numbers,
    complex_decision,
    complex_function,
    exception_handling,
    read_config,
)


def test_add_numbers():
    result = add_numbers(2, 3)
    assert result == 5


def test_complex_decision():
    assert complex_decision(5) == "0 < x <= 10"
    assert complex_decision(15) == "10 < x <= 20"
    assert complex_decision(25) == "x > 20"
    assert complex_decision(-5) == "x <= 0"


def test_exception_handling():
    # We know the function will suppress the exception, so no exception should propagate
    exception_handling()


def test_complex_function():
    data = [[5, 15], [25, 3]]
    result = complex_function(data)
    assert result == [5, 0, 15, 30, 45, 60, 0, 25, 50, 75, 100, 3]
