import pytest

from src.warikan_models.money import Money

def test_money():
    assert Money(100) == Money(100)
    assert Money(100) + Money(200) == Money(300)
    assert Money(100) - Money(200) == Money(-100)


# assert to throw some error when adding/subtracting/multiplying/dividing Money and int
def test_throw_money_with_int():
    with pytest.raises(AttributeError):
        Money(100) + 100
    with pytest.raises(AttributeError):
        Money(100) - 100
    with pytest.raises(TypeError):
        Money(100) * 100
    with pytest.raises(TypeError):
        Money(100) / 100


# assert to throw TypeError when adding/subtracting/multiplying/dividing Money and float
def test_throw_money_with_float():
    with pytest.raises(AttributeError):
        Money(100) + 100.0
    with pytest.raises(AttributeError):
        Money(100) - 100.0
    with pytest.raises(TypeError):
        Money(100) * 100.0
    with pytest.raises(TypeError):
        Money(100) / 100.0
