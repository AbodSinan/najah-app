from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from booking.models import BookingStatus

from payment.models import Payment, PaymentStatus

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
