from decimal import Decimal
from django.db import models

from enumfields import EnumField

from education.models import BaseModel
from payment.enums import PaymentType, PaymentStatus

class PaymentType(models.TextChoices):
    CASH  = ("C", "Cash payment")

class PaymentStatus(models.IntegerChoices):
    INITIATED = 10
    PENDING = 20
    PAID = 30
    CANCELLED = -10

class Payment(BaseModel):
    type = models.CharField(PaymentType, max_length=2, choices=PaymentType.choices, default=PaymentType.CASH)
    status = models.IntegerField(PaymentStatus, choices=PaymentStatus.choices, default=PaymentStatus.INITIATED)
    amount = models.DecimalField(max_digits=15, decimal_places=0, default=Decimal("0.00"))
