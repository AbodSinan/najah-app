from django.urls import path
from rest_framework.routers import DefaultRouter

from profile.views import UpdateProfileView, RetrieveProfileView

app_name="profile"

url_patterns = [
  path("", UpdateProfileView.as_view(), name="profile"),
  path("get-profile/<pk>", RetrieveProfileView.as_view(), name="get_profile"),
]


