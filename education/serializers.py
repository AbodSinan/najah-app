from rest_framework import serializers

from education.models import Subject, SubjectCategory, SubjectTag, EducationLevel

class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = "__all__"

class SubjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTag
        fields = "__all__"

class SubjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCategory
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    subject_category = serializers.PrimaryKeyRelatedField(queryset=SubjectCategory.objects.all())
    subject_tags = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=SubjectTag.objects.all())
    class Meta:
        model = Subject
        fields = "__all__"
 