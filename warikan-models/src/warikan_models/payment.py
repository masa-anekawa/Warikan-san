from dataclasses import dataclass
from datetime import datetime

from src.warikan_models.money import Money
from src.warikan_models.user import User

@dataclass(frozen=True)
class Payment():
    """支払い情報"""
    payer: User
    payee: User
    item: str
    amount: Money
    paid_at: datetime
