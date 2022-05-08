from booking.tests.factories import AcademyClassFactory
from profile.tests.factories import ProfileFactory
from rest_framework.test import APITestCase
from profile.models import UserType

class BookingModelTestCases(APITestCase):
  def setUp(self):
    self.student_set = [ProfileFactory(user_type = UserType.STUDENT) for x in range(3)]
    self.cls = AcademyClassFactory(student_capacity=3, students=self.student_set)
  
  def test_class_student_capacity(self):
    self.assertEqual(self.cls.capacity_ratio, "3/3")
