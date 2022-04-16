from statistics import mode
from django.db import models

from enumfields import EnumField

from booking.enums import FrequencyEnum
from education.models import BaseModel, Subject, EducationLevel
from payment.models import Payment
from persons.models import Student, Tutor

class Class(BaseModel):
    duration = models.DecimalField(decimal_places=2,max_digits=4)
    frequency = EnumField(FrequencyEnum)
    no_of_times = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT)
    students = models.ManyToManyField(Student)
    education_level = models.ForeignKey(EducationLevel)

class Booking(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    booking_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    