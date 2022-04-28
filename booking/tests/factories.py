import factory

from booking.models import Class, Booking
from profile.tests.factories import ProfileFactory
from payment.tests.factories import PaymentFactory

class ClassFactory(factory.django.DjangoModelFactory):
    tutor = factory.SubFactory(ProfileFactory)
    class Meta:
        model = Class

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for tag in extracted:
                self.students.add(tag)

class BookingFactory(factory.django.DjangoModelFactory):
    payment = factory.SubFactory(PaymentFactory)
    class Meta:
        model = Booking
