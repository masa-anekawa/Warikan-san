import copy
import pytest

from src.warikan_models.money import Money
from src.warikan_models.payment import Payment
from src.warikan_models.remittance import Remittance

def test_payment_is_value_object(payment_1):
    copied_payment = copy.deepcopy(payment_1)
    assert payment_1 == copied_payment


def test_payment_is_immutable(payment_1):
    with pytest.raises(AttributeError):
        payment_1.payer = 'fuga'
    with pytest.raises(AttributeError):
        payment_1.item = 'item2'
    with pytest.raises(AttributeError):
        payment_1.amount = Money(2000)
    with pytest.raises(AttributeError):
        payment_1.paid_at = '2021-01-02'
