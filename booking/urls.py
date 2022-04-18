from rest_framework.routers import DefaultRouter
from django.urls import path

from booking.views import ClassBookingListView, SubjectClassListView

app_name = "booking"

api_router = DefaultRouter()

url_patterns = [
    path("class-bookings/<int:booking_class>", ClassBookingListView.as_view(), name="class_bookings"),
    path("subject-classes/<int:subject_id>", SubjectClassListView.as_view(), name="subject_classes")
]

url_patterns+= api_router.urls
