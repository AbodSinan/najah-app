from django.db import models
from django.contrib.auth.models import User

from enumfields import EnumField

from education.models import EducationLevel, BaseModel
from profile.enums import Gender

class UserType(models.TextChoices):
    STUDENT = ("S", "Student")
    TUTOR = ("T", "Tutor")

class Profile(BaseModel):
    """ An extension to the user model, containing more info """
    user_type = models.CharField(max_length=1, choices=UserType.choices, default=UserType.STUDENT)
    age = models.IntegerField(null=True)
    gender = EnumField(Gender, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(null=True)

    def __str__(self) -> str:
        return f"{self.user.email}:{self.user.first_name} ({self.user_type})"
