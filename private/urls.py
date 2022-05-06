from django.urls import path
from rest_framework import routers

from private.views import PrivateClassViewSet, StudentPrivateClassViewSet, TutorPrivateClassOfferViewSet, ConfirmPrivateClassTutorView

app_name = "education"

api_router = routers.DefaultRouter()
api_router.register(
  "tutor-offers",
  TutorPrivateClassOfferViewSet,
  basename="tutor_offers"
)
api_router.register(
  "private-classes",
  PrivateClassViewSet,
  basename="private_classes"
)
api_router.register(
  "student-private-classes",
  StudentPrivateClassViewSet,
  basename="student_private-classes"
)

url_patterns = [
  path("select-tutor/", ConfirmPrivateClassTutorView.as_view(), name="select_tutor")
]

url_patterns += api_router.urls
