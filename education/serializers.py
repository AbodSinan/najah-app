from yaml import serialize
from rest_framework import serializers

from education.models import Subject, SubjectCategory


class SubjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCategory

class SubjectSerializer(serializers.ModelsSerializer):
    class Meta:
        model = Subject
 