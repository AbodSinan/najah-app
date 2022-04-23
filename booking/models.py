from decimal import Decimal
from django.db import models

from enumfields import EnumField

from booking.enums import FrequencyEnum
from education.models import BaseModel, Subject, EducationLevel
from payment.models import Payment
from profile.models import Profile

class FrequencyChoices(models.TextChoices):
    DAILY = ("D", "Daily")
    WEEKLY = ("W", "Weekly")
    MONTHLY = ("M", "Monthly")

class Class(BaseModel):
    duration = models.DecimalField(decimal_places=2,max_digits=4)
    frequency = models.CharField(max_length=1, choices=FrequencyChoices.choices, null=False)
    no_of_times = models.IntegerField(null=False)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, null=True)
    tutor = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="classes_tutored")
    students = models.ManyToManyField(Profile, related_name="classes_joined")
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)
    rate_per_hour = models.DecimalField(decimal_places=2, max_digits=15, default=Decimal("0.00"))
    description = models.TextField(null=True)

    @property
    def price_per_session(self):
        return Decimal(self.rate_per_hour * self.duration)

    @property
    def total_price(self):
        return Decimal(self.price_per_session * self.no_of_times)

    def __str__(self) -> str:
        return f"({self.id}){self.tutor}:{self.subject}"

class Booking(BaseModel):
    student = models.ForeignKey(Profile, on_delete=models.PROTECT)
    booking_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.student}: {self.booking_class}"
    