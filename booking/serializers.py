from rest_framework import serializers

from booking.models import Booking, Class

from persons.serializers import StudentSerializer, TutorSerializer


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class ClassSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()
    students = StudentSerializer(many=True)
    class Meta:
        model = Class
        fields = "__all__"
