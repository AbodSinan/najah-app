from ast import Sub
from unicodedata import category
from rest_framework import serializers

from education.models import Subject, SubjectCategory, SubjectTag

class SubjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTag
        fields = "__all__"

class SubjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCategory
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    subject_category = SubjectCategorySerializer()
    subject_tags = SubjectTagSerializer(many=True)
    class Meta:
        model = Subject
        fields = "__all__"
 