from rest_framework import serializers

from persons.models import Tutor, Student

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = "__all__"

class StudentSerializer(serializers.StudentSerializer):
    class Meta:
        model = Student
        fields = "__all__"