from rest_framework.routers import DefaultRouter
from django.urls import path

from booking.views import AcceptClassBookingView,ClassBookingListView, AcademyClassListView, SubjectClassListView, UserClassListCreateView

app_name = "booking"

api_router = DefaultRouter()

url_patterns = [
    path("class-bookings/<int:booking_class>", ClassBookingListView.as_view(), name="class_bookings"),
    path("subject-classes/<int:subject_id>", SubjectClassListView.as_view(), name="subject_classes"),
    path("user-classes", UserClassListCreateView.as_view(), name="user_classes"),
    path("classes", AcademyClassListView.as_view(), name="class_list"),
    path("accept-booking", AcceptClassBookingView.as_view(), name="accept_booking"),
]

url_patterns+= api_router.urls
