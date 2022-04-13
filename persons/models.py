from django.db import models

from enumfields import EnumField

from education.models import EducationLevel, BaseModel
from persons.enums import Gender

class Person(BaseModel):
    """ An abstract model representing a person entity"""
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = EnumField(Gender)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

class Student(Person):
    school = models.CharField(max_length=50)

class Tutor(BaseModel):
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)