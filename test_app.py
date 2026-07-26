from app import add, multiply, subtract


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
