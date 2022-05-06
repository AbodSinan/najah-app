from rest_framework import serializers

from profile.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    education_level = serializers.CharField(source="education_level.name")

    class Meta:
        model = Profile
        fields = "__all__"
