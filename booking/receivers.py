from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from booking.models import Booking, BookingStatus

from payment.models import Payment, PaymentStatus, PaymentType

@receiver(post_save, sender=Booking)
def process_booking(sender, **kwargs):
  instance = kwargs.get("instance")

  if instance.status == BookingStatus.PENDING_PAYMENT and not instance.payment:
    if settings.SKIP_PAYMENT:
      instance.status = BookingStatus.CONFIRMED
      instance.save()
    else:
      payment = Payment.objects.create(
          amount=instance.booking_class.total_price,
          type=PaymentType.CASH
      )
      instance.payment = payment
      instance.save()

@receiver(post_save, sender=Payment)
def confirm_student_class_payment(sender, **kwargs):
  """Add the student to the class once the payment is done"""
  instance = kwargs.get("instance")

  if instance.status == PaymentStatus.PAID:
    booking = instance.booking
    booking.status = BookingStatus.CONFIRMED
    booking.save()
    booking_class = booking.booking_class
    booking_class.students.add(booking.student)

  if instance.status == PaymentStatus.CANCELLED:
    booking = instance.booking
    booking.status = BookingStatus.CANCELLED
    booking.save()
