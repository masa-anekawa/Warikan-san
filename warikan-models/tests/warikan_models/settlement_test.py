import copy
import pytest

from src.warikan_models.settlement import Settlement
from src.warikan_models.user import User
from src.warikan_models.payment import Payment
from src.warikan_models.money import Money

def test_settlement_is_value_object(settlement_for_payment_1_and_2):
    copied_settlement = copy.deepcopy(settlement_for_payment_1_and_2)
    assert settlement_for_payment_1_and_2 == copied_settlement


def test_settlement_can_only_be_constructed_by_a_list_of_payments(payment_1, user_1):
    with pytest.raises(ValueError):
        Settlement(set())
    with pytest.raises(ValueError):
        Settlement({})
    with pytest.raises(ValueError):
        Settlement([])
    assert Settlement([payment_1])

    # assert to throw when construct with a set and other parameters
    with pytest.raises(TypeError):
        Settlement([payment_1], sender=user_1)
    with pytest.raises(TypeError):
        Settlement([payment_1], receiver=user_1)
    with pytest.raises(TypeError):
        Settlement([payment_1], amount=Money(100))
    with pytest.raises(TypeError):
        Settlement([payment_1], settled_at='2021-01-01')
    with pytest.raises(TypeError):
        Settlement([payment_1], is_settled=True)


def test_settlement_calculates_remittance(payment_1, payment_2, remittance_from_user_1_to_2_by_1000, remittance_from_user_2_to_1_by_1000):
    settlement = Settlement([payment_1, payment_2])
    assert settlement.remittance == remittance_from_user_1_to_2_by_1000

    another_settlement = Settlement([payment_1])
    assert another_settlement.remittance == remittance_from_user_2_to_1_by_1000