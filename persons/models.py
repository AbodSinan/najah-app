from django.db import models
from django.contrib.auth.models import User

from enumfields import EnumField

from education.models import EducationLevel, BaseModel
from persons.enums import Gender

#TODO: Add user to person model and establish logic

class Person(BaseModel):
    """ An abstract model representing a person entity"""
    name = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    gender = EnumField(Gender, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

class Student(Person):
    school = models.CharField(max_length=50)

class Tutor(Person):
    description = models.TextField(null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)