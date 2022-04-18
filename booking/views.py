from rest_framework import generics
from rest_framework.exceptions import ValidationError

from booking.models import Class, Booking
from booking.serializers import BookingSerializer, ClassSerializer
from profile.models import UserType


class ClassBookingListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        if self.request.user.profile.user_type == UserType.TUTOR:
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
    serializer_class = ClassSerializer

    def get_queryset(self):
        return Class.objects.filter(
            subject__id=self.kwargs["subject_id"],
        )

    def get_serializer_context(self):
        context= super().get_serializer_context()
        context["subject_id"] = self.kwargs["subject_id"]
        context["profile"] = self.request.user.profile

        return context

    def perform_create(self, serializer):
        if not self.request.user or self.request.user.profile.user_type == UserType.STUDENT:
            raise ValidationError("Students cannot create a class!")
        else:
            return super().perform_create(serializer)
