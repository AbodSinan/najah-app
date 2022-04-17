from django.contrib.auth.models import User
from django.db import models

class UserType(models.TextChoices):
    STUDENT = ("S", "Student")
    TUTOR = ("T", "Tutor")

class CustomUser(User):
    user_type = models.CharField(max_length=1, choices=UserType.choices)
