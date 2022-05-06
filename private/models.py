from decimal import Decimal

from django.db import models

from education.models import BaseModel, Subject, EducationLevel
from profile.models import Profile

class PrivateClassStatus(models.IntegerChoices):
  PENDING_TUTOR_SELECTION = 10
  ONGOING = 20
  COMPLETE = 30

class PrivateClassOfferStatus(models.IntegerChoices):
  PENDING = 10
  CANCELLED = 20
  ACCEPTED = 30

# Create your models here.
class PrivateClass(BaseModel):
  education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)
  subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
  student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="studied_private_classes")
  description = models.TextField()
  tutor = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name="tutored_private_classes")
  status = models.IntegerField(choices=PrivateClassStatus.choices, default=PrivateClassStatus.PENDING_TUTOR_SELECTION)
  rate = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal("0.00"))

  @property
  def education_level_name(self):
    return self.education_level.name

  def __str__(self) -> str:
      return f"{self.student.full_name}: {self.subject.name}"


class PrivateClassOffer(BaseModel):
  tutor = models.ForeignKey(Profile, on_delete=models.CASCADE)
  private_class = models.ForeignKey(PrivateClass, on_delete=models.CASCADE)
  status = models.IntegerField(choices=PrivateClassOfferStatus.choices, default=PrivateClassOfferStatus.PENDING)

  class Meta:
    unique_together = ("tutor", "private_class")
  
  