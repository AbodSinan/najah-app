from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    class Meta:
        abstract = True

class EducationLevel(models.Model):
    """ To store the information for the educational level (e.g. school, bachelor, diploma, etc.)"""
    name = models.CharField(max_length=30)
    is_higher_education = models.BooleanField()

class SubjectCategory(models.Model):
    """ A model to store category of subjects (e.g. medical, history, engineering)"""
    name = models.CharField(max_length=30)

class SubjectTag(models.Model):
    """ A model to store tags of a subject (e.g. co-curricular, primary, final-year, project, practical, etc.)"""
    name = models.CharField(max_length=30)

class Subject(models.Model):
    """ A model to store information about a subject"""
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    subject_tags = models.ManyToManyField(SubjectTag)
    subject_category = models.ForeignKey(SubjectCategory, on_delete=models.SET_NULL, null=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)
