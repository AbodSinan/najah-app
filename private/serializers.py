from rest_framework import serializers

from private.models import PrivateClass, PrivateClassOffer
from profile.serializers import ProfileSerializer

class PrivateClassOfferSerializer(serializers.ModelSerializer):
  tutor = ProfileSerializer()

  class Meta:
    model = PrivateClassOffer
    fields = "__all__"

class PrivateClassSerializer(serializers.ModelSerializer):
  class Meta:
    model = PrivateClass
    fields = "__all__"

class StudentPrivateClassSerializer(serializers.ModelSerializer):
  tutor_offers = PrivateClassOfferSerializer(many=True, source="privateclassoffer_set")
  
  class Meta:
    model = PrivateClass
    fields = "__all__"
