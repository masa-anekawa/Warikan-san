from datetime import datetime
from dataclasses import dataclass, field
from decimal import Decimal

from src.warikan_models.payment import Payment
from src.warikan_models.user import User
from src.warikan_models.remittance import Remittance
from src.warikan_models.money import Money


@dataclass
class Settlement():
    """精算情報"""
    payments: list[Payment]
    participants: set[User] = field(default_factory=set)
    remittance: Remittance = None
    settled_at: datetime = None
    is_settled: bool = False

    # This class can only be constructed by a list of payments
    def __init__(self, payments: list[Payment]):
        # The set of payments must not be empty
        if len(payments) == 0:
            raise ValueError('The set of payments must not be empty')
        self.payments = payments
        # For now participants are just 2 ppl, the payer and the payee of the first payment
        self.participants = [payments[0].payer, payments[0].payee]
        self.__calculate_remittance()

    # calculate the total amount of payments, and determine the sender and receiver by
    def __calculate_remittance(self):
        tmp_sender = self.payments[0].payee
        total_money = Money(Decimal(0))
        for payment in self.payments:
            if payment.payee == tmp_sender:
                total_money += payment.amount
            else:
                total_money -= payment.amount
        if total_money.amount > 0:
            sender = tmp_sender
            receiver = self.payments[0].payer
            amount = total_money
        elif total_money.amount < 0:
            sender = self.payments[0].payer
            receiver = tmp_sender
            amount =  Money(total_money.amount * -1)
        else:
            print('The total amount of payments is zero. This rarely happens and should be checked.')
            sender = tmp_sender
            receiver = self.payments[0].payer
            amount = total_money
        self.remittance = Remittance(sender, receiver, amount)

