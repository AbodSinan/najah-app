from decimal import Decimal
from django.db import models

from education.models import BaseModel, Subject, EducationLevel
from payment.models import Payment
from profile.models import Profile

class FrequencyChoices(models.TextChoices):
    DAILY = ("D", "Daily")
    WEEKLY = ("W", "Weekly")
    MONTHLY = ("M", "Monthly")

class ClassStatus(models.TextChoices):
    PENDING = ("P", "Pending Registration")
    PENDING_TUTOR = ("T", "Pending Tutor Selection")
    STARTED = ("S", "Class has started")
    ENDED = ("E", "Class Has Ended")
    CANCELLED = ("C", "Cancelled")

class Class(BaseModel):
    """
    An abstract model containing information about a class, shared between academic and private classes
    """
    duration = models.DecimalField(decimal_places=2,max_digits=4, default=Decimal("0.00"))
    frequency = models.CharField(max_length=1, choices=FrequencyChoices.choices, null=True)
    no_of_times = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, null=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)
    rate_per_hour = models.DecimalField(decimal_places=2, max_digits=15, default=Decimal("0.00"))
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    status = models.CharField(max_length = 2, choices = ClassStatus.choices, default=ClassStatus.PENDING)
    is_remote = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def education_level_name(self):
        return self.education_level.name

    @property
    def price_per_session(self):
        return Decimal(self.rate_per_hour * self.duration)

    @property
    def total_price(self):
        return Decimal(self.price_per_session * self.no_of_times)
    
    @property
    def capacity_ratio(self):
        return f"{self.students.count()}/{self.student_capacity}"

    def __str__(self) -> str:
        return f"({self.id}){self.tutor}:{self.subject}"

class AcademyClass(Class):
    """
    A model to store information about academy classes, where a tutor opens a class and students join
    """
    students = models.ManyToManyField(Profile, related_name="classes_enrolled")
    student_capacity = models.PositiveSmallIntegerField(null = True)
    tutor = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="classes_tutored")

class BookingStatus(models.IntegerChoices):
    PENDING = 10
    CONFIRMED = 20
    CANCELLED = -10

class Booking(BaseModel):
    """
    A model to store booking infomation of a student in a certain class
    """
    student = models.ForeignKey(Profile, on_delete=models.PROTECT)
    booking_class = models.ForeignKey(AcademyClass, on_delete=models.PROTECT)
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT)
    status = models.IntegerField(BookingStatus, choices=BookingStatus.choices, default=BookingStatus.PENDING)


    def __str__(self) -> str:
        return f"{self.student}: {self.booking_class}"
    