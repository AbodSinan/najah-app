from ast import Sub
from django.contrib import admin

from education.models import EducationLevel, Subject, SubjectCategory, SubjectTag

# Register your models here.
admin.site.register(EducationLevel)
admin.site.register(Subject)
admin.site.register(SubjectCategory)
admin.site.register(SubjectTag)
