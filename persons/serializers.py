from rest_framework import serializers

from persons.models import Tutor, Student

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor

class StudentSerializer(serializers.StudentSerializer):
    class Meta:
        model = Student