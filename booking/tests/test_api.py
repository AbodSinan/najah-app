from decimal import Decimal

from django.urls import reverse
from education.tests.factories import EducationLevelFactory, SubjectFactory

from rest_framework.test import APITestCase

from payment.models import Payment
from profile.tests.factories import ProfileFactory, TokenFactory
from profile.models import UserType
from booking.models import AcademyClass, Booking
from booking.tests.factories import AcademyClassFactory, BookingFactory

class TestBookingViewSet(APITestCase):
    def setUp(self):
        self.education_level = EducationLevelFactory()
        self.tutor_profile = ProfileFactory(user_type=UserType.TUTOR, education_level=self.education_level)
        self.student_profile1 = ProfileFactory(user_type=UserType.STUDENT, education_level=self.education_level)
        self.student_profile2 = ProfileFactory(user_type=UserType.STUDENT, education_level=self.education_level)
        self.subject = SubjectFactory(education_level=self.education_level)
        self.subject_class = AcademyClassFactory(subject=self.subject, tutor=self.tutor_profile, duration=Decimal("1.50"), frequency="W", no_of_times=2, rate_per_hour= Decimal("10.00"))
        self.subject_class2 = AcademyClassFactory(subject=self.subject, tutor=self.tutor_profile, duration=Decimal("1.50"), frequency="W", no_of_times=2, rate_per_hour= Decimal("10.00"))
        self.booking1 = BookingFactory(booking_class=self.subject_class, student=self.student_profile1)
        self.booking2 = BookingFactory(booking_class=self.subject_class, student=self.student_profile2)

        self.token = TokenFactory(user = self.tutor_profile.user)

    def test_list_class_booking(self):
        self.client.force_authenticate(user = self.tutor_profile.user, token=self.token)
        url = reverse("booking:class_bookings", kwargs={"booking_class": self.subject_class.pk})
        resp = self.client.get(url)
        resp_data = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp_data), 2)

    def test_list_class_booking_another_tutor(self):
        new_tutor_profile = ProfileFactory(user_type=UserType.TUTOR, education_level=self.education_level)
        token = TokenFactory(user = new_tutor_profile.user)
        url = reverse("booking:class_bookings", kwargs={"booking_class": self.subject_class.pk})
        resp = self.client.get(url, HTTP_AUTHORIZATION=f"Token {token.key}")
        
        self.assertEqual(len(resp.json()), 0)

    def test_create_booking_by_student(self):
        student_token = TokenFactory(user = self.student_profile1.user)
        url = reverse("booking:class_bookings", kwargs={"booking_class": self.subject_class.pk})
        req = {}

        resp = self.client.post(url, data=req, HTTP_AUTHORIZATION=f"Token {student_token.key}")
        
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["payment"]["amount"], "30")

        last_class = AcademyClass.objects.get(id=self.subject_class.pk)

        self.assertEqual(Booking.objects.filter(booking_class=last_class).count(), 3)
        self.assertEqual(Payment.objects.count(), 3)

    def test_list_classes_subject(self):
        url = reverse("booking:subject_classes", kwargs={"subject_id": self.subject.pk})

        resp = self.client.get(url, HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)
        
    def test_create_class_tutor(self):
        url = reverse("booking:subject_classes", kwargs={"subject_id": self.subject.pk})
        req = {
            "duration": Decimal("1.50"),
            "students": [],
            "frequency": "W",
            "no_of_times": 8,
            "rate_per_hour": Decimal("15.00")
        }

        resp = self.client.post(url, data=req, HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.assertEqual(resp.status_code, 201)
    
    def test_create_class_student(self):
        student_token = TokenFactory(user = self.student_profile1.user)
        url = reverse("booking:subject_classes", kwargs={"subject_id": self.subject.pk})
        req = {
            "duration": Decimal("1.50"),
            "students": [],
            "frequency": "W",
            "no_of_times": 8,
            "rate_per_hour": Decimal("15.00")
        }

        resp = self.client.post(url, data=req, HTTP_AUTHORIZATION=f"Token {student_token.key}")
        
        self.assertEqual(resp.status_code, 400)

    def test_list_user_classes(self):
        # Create a bunch of new classes, tutors and students
        tutor_profile2 = ProfileFactory(user_type=UserType.TUTOR, education_level=self.education_level)
        subject_class3 = AcademyClassFactory(subject=self.subject, tutor=tutor_profile2, duration=Decimal("1.50"), frequency="W", no_of_times=2, rate_per_hour= Decimal("10.00"))
        self.subject_class.students.add(self.student_profile1)
        self.subject_class2.students.add(self.student_profile2)
        subject_class3.students.add(self.student_profile1)
        subject_class3.students.add(self.student_profile2)

        tutor2_token = TokenFactory(user = tutor_profile2.user)
        student1_token = TokenFactory(user = self.student_profile1.user)

        url = reverse("booking:user_classes")

        # Test retrieving classes for a student
        resp1 = self.client.get(url, HTTP_AUTHORIZATION=f"Token {tutor2_token}")
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(len(resp1.json()), 1)
        self.assertEqual(resp1.json()[0]["id"], subject_class3.id)

        resp2 = self.client.get(url, HTTP_AUTHORIZATION=f"Token {student1_token}")
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(len(resp2.json()), 2)
        
        cls_ids = [x["id"] for x in resp2.json()]
        self.assertCountEqual(cls_ids, [self.subject_class.id, subject_class3.id])
