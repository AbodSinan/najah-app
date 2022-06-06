from django.shortcuts import render

from rest_framework import generics

from profile.models import Profile
from profile.serializers import ProfileSerializer

# Create your views here.
class UpdateProfileView(generics.RetrieveUpdateAPIView):
  serializer_class = ProfileSerializer

  def get_queryset(self):
    return self.request.user.profile


class RetrieveProfileView(generics.RetrieveAPIView):
  serializer_class = ProfileSerializer
  queryset = Profile.objects.all()
