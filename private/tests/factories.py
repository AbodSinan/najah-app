import factory

from education.tests.factories import EducationLevelFactory, SubjectFactory
from private.models import PrivateClass
from profile.tests.factories import ProfileFactory

class PrivateClassFactory(factory.django.DjangoModelFactory):
  subject = factory.SubFactory(SubjectFactory)
  education_level = factory.SubFactory(EducationLevelFactory)
  student = factory.SubFactory(ProfileFactory)

  class Meta:
    model = PrivateClass
