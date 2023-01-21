from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from education.models import EducationLevel, BaseModel

class UserType(models.TextChoices):
    STUDENT = ("S", "Student")
    TUTOR = ("T", "Tutor")

class Gender(models.TextChoices):
    MALE = ("M", "Male")
    FEMALE = ("F", "Female")

class Profile(BaseModel):
    """ An extension to the user model, containing more info """
    uuid = models.UUIDField(unique=True, default=uuid4)
    user_type = models.CharField(max_length=1, choices=UserType.choices, default=UserType.STUDENT)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.MALE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)
    description = models.TextField(default="")
    image = models.ImageField(null=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name
    
    @property
    def email(self):
        return self.user.email

    def __str__(self) -> str:
        return f"{self.user.email}:{self.user.first_name} ({self.user_type})"
