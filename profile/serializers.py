from rest_framework import serializers

from profile.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    age = serializers.IntegerField(required=False)
    education_level = serializers.CharField(source="education_level.name", required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    def update(self, instance, validated_data):
        # Update fields regarding the user
        instance.user.first_name = validated_data.pop("first_name", instance.user.first_name)
        instance.user.last_name = validated_data.pop("last_name", instance.user.last_name)
        instance.user.email = validated_data.pop("email", instance.user.email)
        instance.user.save()
        
        # Update the rest
        return super().update(instance, validated_data)
