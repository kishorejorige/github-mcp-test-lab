from app import add


def test_add():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


def test_add_zero():
    assert add(0, 5) == 5


def test_add_mixed_numbers():
    assert add(-2, 7) == 5
