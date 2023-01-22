from django.conf import settings
from django.db.models import Q

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from booking.models import AcademyClass, Booking, BookingStatus
from booking.serializers import BookingSerializer, AcademyClassSerializer, AcceptClassBookingSerializer, UpdateClassStatusSerializer
from profile.models import UserType
from private.models import PrivateClass


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
            return AcademyClass.objects.filter(Q(tutor__user=self.request.user)|Q(students__user=self.request.user)).distinct()

class AcademyClassListView(generics.ListAPIView):
    serializer_class = AcademyClassSerializer
    queryset = AcademyClass.objects.all()

class AcceptClassBookingView(views.APIView):
    def post(self, request):
        serializer = AcceptClassBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking_id = serializer.data.get("booking_id", None)

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Invalid booking_id"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Only allow tutors to accept/reject bookings
        if self.request.user.profile.id != booking.booking_class.tutor.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        is_accepted = serializer.data.get("is_accepted", None)

        booking.status = BookingStatus.PENDING_PAYMENT if is_accepted else BookingStatus.CANCELLED
        booking.save()

        return Response(status=status.HTTP_200_OK)

class UpdateClassStatusView(views.APIView):
    def post(self, request):
        serializer = UpdateClassStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_id = serializer.data.get("class_id", None)
        class_type = serializer.data.get("class_type", "academy")
        if class_type == "academy":
            try:
                cls = AcademyClass.objects.get(id=class_id)
            except AcademyClass.DoesNotExist:
                return Response({"error": "Invalid booking_id"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            # Only allow tutors to update status for academy classes
            if self.request.user.profile.id != cls.tutor.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        if class_type == "private":
            try:
                cls = PrivateClass.objects.get(id=class_id)
            except PrivateClass.DoesNotExist:
                return Response({"error": "Invalid booking_id"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            # Only allow students to update status for private classes
            if self.request.user.profile.id != cls.student.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        

        status = serializer.data.get("status", None)

        cls.status = status
        cls.save()

        return Response(status=status.HTTP_200_OK)
