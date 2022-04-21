from rest_framework import serializers

from profile.serializers import ProfileSerializer

class PrivateClassOfferSerializer(serializers.ModelSerializer):
  tutor = ProfileSerializer()

  class Meta:
    fields = "__all__"

class PrivateClassSerializer(serializers.ModelSerializer):
  tutor_offers = PrivateClassOfferSerializer(many=True, source="privateclassoffer_set")
  
  class Meta:
    fields = "__all__"
