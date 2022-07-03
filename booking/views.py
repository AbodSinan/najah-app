from django.conf import settings
from django.db.models import Q

from rest_framework import generics
from rest_framework.exceptions import ValidationError

from booking.models import AcademyClass, Booking
from booking.serializers import BookingSerializer, AcademyClassSerializer
from profile.models import UserType


class ClassBookingListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        if not settings.IS_USER_TYPE_ENABLED or self.request.user.profile.user_type == UserType.TUTOR:
            return Booking.objects.filter(
                booking_class=self.kwargs["booking_class"],
                booking_class__tutor=self.request.user.profile,
            )
        else:
            return None
    
    def get_serializer_context(self):
        context= super().get_serializer_context()
        context["booking_class"] = self.kwargs["booking_class"]
        context["student"] = self.request.user.profile

        return context


class SubjectClassListView(generics.ListCreateAPIView):
    serializer_class = AcademyClassSerializer

    def get_queryset(self):
        return AcademyClass.objects.filter(
            subject__id=self.kwargs["subject_id"],
        )

    def get_serializer_context(self):
        context= super().get_serializer_context()
        context["subject_id"] = self.kwargs["subject_id"]
        context["profile"] = self.request.user.profile

        return context

    def perform_create(self, serializer):
        if settings.IS_USER_TYPE_ENABLED and self.request.user.profile.user_type == UserType.STUDENT:
            raise ValidationError("Students cannot create a class!")
        else:
            return super().perform_create(serializer)

class UserClassListCreateView(generics.ListCreateAPIView):
    serializer_class = AcademyClassSerializer

    def get_queryset(self):
        if settings.IS_USER_TYPE_ENABLED:
            if self.request.user.profile.user_type == UserType.TUTOR:
                return AcademyClass.objects.filter(tutor__user=self.request.user)
            else:
                return AcademyClass.objects.filter(students__user=self.request.user)
        else:
            return AcademyClass.objects.filter(Q(tutor__user=self.request.user)|Q(students__user=self.request.user))

class AcademyClassListView(generics.ListAPIView):
    serializer_class = AcademyClassSerializer
    queryset = AcademyClass.objects.all()
