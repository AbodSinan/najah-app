from decimal import Decimal
from django.db import models

from enumfields import EnumField

from education.models import BaseModel
from payment.enums import PaymentType, PaymentStatus

class Payment(BaseModel):
    type = EnumField(PaymentType)
    status = EnumField(PaymentStatus)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
