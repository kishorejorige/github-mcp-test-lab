import pytest

from app import add, divide, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


def test_add_zero():
    assert add(0, 5) == 5


def test_add_mixed_numbers():
    assert add(-2, 7) == 5


def test_subtract():
    assert subtract(5, 2) == 3


def test_subtract_negative_result():
    assert subtract(2, 5) == -3


def test_multiply():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(5, 0) == 0


def test_divide():
    assert divide(10, 2) == 5


def test_divide_decimal_result():
    assert divide(5, 2) == 2.5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
