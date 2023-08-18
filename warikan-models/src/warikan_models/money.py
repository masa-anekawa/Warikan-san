from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money():
    amount: Decimal
    currency: str = 'JPY'

    # Force the use of the constructor to be without currency
    def __post_init__(self):
        if self.currency != 'JPY':
            raise ValueError('Currency must be JPY')

    def __add__(self, other):
        return Money(self.amount + other.amount)

    def __sub__(self, other):
        return Money(self.amount - other.amount)
