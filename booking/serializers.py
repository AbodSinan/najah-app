from rest_framework import serializers

from booking.models import Booking, Class


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
