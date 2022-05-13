import factory

from booking.models import AcademyClass, Booking
from profile.tests.factories import ProfileFactory
from payment.tests.factories import PaymentFactory

class AcademyClassFactory(factory.django.DjangoModelFactory):
    tutor = factory.SubFactory(ProfileFactory)
    class Meta:
        model = AcademyClass

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
