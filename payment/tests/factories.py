import factory

from payment.models import Payment, PaymentStatus, PaymentType

class PaymentFactory(factory.django.DjangoModelFactory):
    status = PaymentStatus.INITIATED
    type = PaymentType.CASH
    class Meta:
        model = Payment