# test_module_1.py

import pytest

from src.sonarissues.module1 import (
    always_returns_same,
    divide_numbers,
    insecure_eval,
    process_data,
)


def test_process_data():
    result = process_data(1, 2, 3, 4, 5, 6, 7)
    assert result == 28


def test_divide_numbers():
    result = divide_numbers(10, 2)
    assert result == 5

    # Testing division by zero should raise an exception
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)


def test_always_returns_same():
    result = always_returns_same()
    assert result == 42


def test_insecure_eval():
    # Testing the insecure eval function with a harmless input
    result = insecure_eval("1 + 1")
    assert result is None
