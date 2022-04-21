from django.db import models
from education.models import BaseModel, Subject, EducationLevel
from profile.models import Profile

# Create your models here.
class PrivateClass(BaseModel):
  education_level = models.ForeignKey(EducationLevel, on_delete=EducationLevel)
  subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
  student = models.ForeignKey(Profile)
  description = models.TextField()
  rate = models.DecimalField(decimal_places=2, max_digits=10)

class PrivateClassOffer(BaseModel):
  tutor = models.ForeignKey(Profile, on_delete=models.CASCADE)
  private_class = models.ForeignKey(PrivateClass, on_delete=models.CASCADE)
  
  