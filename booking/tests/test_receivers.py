from django.test import TestCase

from booking.models import BookingStatus
from booking.tests.factories import BookingFactory, AcademyClassFactory
from payment.models import PaymentStatus
from profile.models import UserType
from profile.tests.factories import ProfileFactory

class BookingReceiverTestCase(TestCase):
  def setUp(self):
    self.student = ProfileFactory(user_type=UserType.STUDENT)
    self.cls = AcademyClassFactory(student_capacity=1)
    self.booking = BookingFactory(booking_class=self.cls, student=self.student)

  def test_payment_made(self):
    payment = self.booking.payment
    payment.status = PaymentStatus.PAID
    payment.save()
    self.booking.refresh_from_db()
    self.cls.refresh_from_db()

    self.assertEqual(self.booking.status, BookingStatus.CONFIRMED.value)
    self.assertEqual(self.cls.students.count(), 1)
