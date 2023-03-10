from rest_framework import serializers

from education.models import EducationLevel
from profile.models import Profile
class EducationLevelNameField(serializers.SerializerMethodField):
    def to_representation(self, value):
        try:
            education_level = EducationLevel.objects.get(id=value.id)
            return education_level.name
        except EducationLevel.DoesNotExist:
            return None

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    age = serializers.IntegerField(required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    def update(self, instance, validated_data):
        # Update fields regarding the user
        instance.user.first_name = validated_data.pop("first_name", instance.user.first_name)
        instance.user.last_name = validated_data.pop("last_name", instance.user.last_name)
        instance.user.email = validated_data.pop("email", instance.user.email)
        instance.user.save()
        if "education_level" in validated_data:
            try:
                education_level = EducationLevel.objects.get(name=validated_data["education_level"])
                instance.education_level = education_level
                instance.save()
            except EducationLevel.DoesNotExist:
                raise serializers.ValidationError("Invalid education level")
        
        # Update the rest
        return super().update(instance, validated_data)
