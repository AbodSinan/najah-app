import factory

from education.models import EducationLevel, Subject, SubjectCategory, SubjectTag

class EducationLevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EducationLevel

class SubjectCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubjectCategory

class SubjectTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubjectTag

class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    @factory.post_generation
    def subject_tags(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for tag in extracted:
                self.subject_tags.add(tag)
