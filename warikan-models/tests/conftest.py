from pytest import fixture
from datetime import datetime

from src.warikan_models.money import Money
from src.warikan_models.payment import Payment
from src.warikan_models.remittance import Remittance
from src.warikan_models.user import User
from src.warikan_models.identity import Identity
from src.warikan_models.settlement import Settlement


# Prepare money fixtures
@fixture
def money_1000():
    return Money(1000)


@fixture
def money_2000():
    return Money(2000)


# Prepare identity fixtures
@fixture
def identity_1():
    return Identity('hoge@example.com', 'hashed_password')


@fixture
def identity_2():
    return Identity('fuga@example.com', 'hashed_password')


# Prepare user fixtures
@fixture
def user_1(identity_1):
    return User(identity_1, 'hoge')


@fixture
def user_2(identity_2):
    return User(identity_2, 'fuga')


# Prepare datetime fixtures
@fixture
def datetime_2021_1_1():
    return datetime(2021, 1, 1)


@fixture
def datetime_2021_1_2():
    return datetime(2021, 1, 2)


# Prepare payment fixtures
@fixture
def payment_1(user_1, user_2, money_1000, datetime_2021_1_1):
    return Payment(user_1, user_2, 'item1', money_1000, datetime_2021_1_1)


@fixture
def payment_2(user_1, user_2, money_2000, datetime_2021_1_2):
    return Payment(user_2, user_1, 'item2', money_2000, datetime_2021_1_2)


# Prepare remittance fixtures
@fixture
def remittance_from_user_1_to_2_by_1000(user_1, user_2, money_1000):
    return Remittance(user_1, user_2, money_1000)


@fixture
def remittance_from_user_2_to_1_by_1000(user_2, user_1, money_1000):
    return Remittance(user_2, user_1, money_1000)


# Prepare settlement fixtures
@fixture
def settlement_for_payment_1_and_2(payment_1, payment_2):
    return Settlement((payment_1, payment_2))


@fixture
def settlement_for_payment_1_only(payment_2, payment_1):
    return Settlement((payment_2, payment_1))
