from django.db import models
from booking.models import AcademyClass
from education.models import BaseModel

# Create your models here.
class Announcement(BaseModel):
  room = models.ForeignKey(AcademyClass, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  body = models.TextField()

class Attachment(BaseModel):
  file = models.FileField()
  Announcement = models.ForeignKey(Announcement)
