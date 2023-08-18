from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

from src.warikan_models.payment import Payment
from src.warikan_models.user import User
from src.warikan_models.money import Money

@dataclass
class Remittance():
    """送金情報"""
    sender: User
    receiver: User
    amount: Money
    is_sent: bool = False
    sent_at: datetime = None
    is_received: bool = False
    received_at: datetime = None


