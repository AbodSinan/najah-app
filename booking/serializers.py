from rest_framework import serializers

from booking.models import AcademyClass, Booking
from education.models import Subject
from payment.models import Payment, PaymentType
from payment.serializers import PaymentSerializer
from profile.serializers import ProfileSerializer


class BookingSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    student = ProfileSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ("payment", "booking_class", "student")

    def create(self, validated_data):
        booking_class = AcademyClass.objects.get(id=self.context["booking_class"])
        # The tutor of a class cannot be a student
        if booking_class.tutor.pk == self.context["student"].pk:
            raise serializers.ValidationError("Tutor cannot book in own class")

        payment = Payment.objects.create(
            amount=booking_class.total_price,
            type=PaymentType.CASH
        )

        booking = Booking.objects.create(
            booking_class = booking_class,
            payment = payment,
            student = self.context["student"]
        )
        
        return booking

class AcademyClassSerializer(serializers.ModelSerializer):
    tutor = ProfileSerializer(read_only=True)
    students = ProfileSerializer(many=True, required=False)
    class Meta:
        model = AcademyClass
        fields = "__all__"
        read_only_fields = ("tutor",)

    def create(self, validated_data):
        
        subject = Subject.objects.get(id=self.context["subject_id"])
        tutor = self.context["profile"]
        
        return AcademyClass.objects.create(
            subject=subject,
            tutor=tutor,
            **validated_data,
        )
