from rest_framework import serializers

from private.models import PrivateClass, PrivateClassOffer
from profile.serializers import ProfileSerializer

class PrivateClassOfferSerializer(serializers.ModelSerializer):
  tutor = ProfileSerializer(read_only=True)

  class Meta:
    model = PrivateClassOffer
    fields = "__all__"

class PrivateClassSerializer(serializers.ModelSerializer):
  education_level_name = serializers.CharField(read_only=True)
  class Meta:
    model = PrivateClass
    fields = "__all__"
    read_only_fields = ("student", "education_level_name")
    extra_kwargs = {
      'education_level': {"write_only": True}
    }

class StudentPrivateClassSerializer(serializers.ModelSerializer):
  tutor_offers = PrivateClassOfferSerializer(many=True, source="privateclassoffer_set")
  
  class Meta:
    model = PrivateClass
    fields = "__all__"
  
class ConfirmTutorSerializer(serializers.Serializer):
  tutor_id = serializers.IntegerField()
  private_class_id = serializers.IntegerField()
