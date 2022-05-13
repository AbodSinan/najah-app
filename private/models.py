from decimal import Decimal

from django.db import models

from booking.models import Class
from education.models import BaseModel
from profile.models import Profile

class PrivateClassStatus(models.IntegerChoices):
  PENDING_TUTOR_SELECTION = 10
  ONGOING = 20
  COMPLETE = 30

class PrivateClassOfferStatus(models.IntegerChoices):
  PENDING = 10
  CANCELLED = 20
  ACCEPTED = 30

class PrivateClass(Class):
  """
  A model storing information about a private class, inherited from the Class abstract model
  """
  tutor = models.ForeignKey(Profile, on_delete=models.SET_NULL,  null=True, related_name="private_classes_tutored")
  student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="studied_private_classes")

  def __str__(self) -> str:
      return f"{self.student.full_name}: {self.subject.name}"


class PrivateClassOffer(BaseModel):
  tutor = models.ForeignKey(Profile, on_delete=models.CASCADE)
  private_class = models.ForeignKey(PrivateClass, on_delete=models.CASCADE)
  status = models.IntegerField(choices=PrivateClassOfferStatus.choices, default=PrivateClassOfferStatus.PENDING)

  class Meta:
    unique_together = ("tutor", "private_class")
  
  