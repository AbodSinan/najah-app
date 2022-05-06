from decimal import Decimal
from django.db import IntegrityError
from django.urls import reverse
from private.tests.factories import PrivateClassFactory

from rest_framework.test import APITestCase

from education.tests.factories import EducationLevelFactory, SubjectFactory
from private.models import PrivateClass, PrivateClassOffer, PrivateClassOfferStatus
from profile.models import UserType
from profile.tests.factories import ProfileFactory, TokenFactory

# Create your tests here.

class PrivateClassesTestCases(APITestCase):
  PRIVATE_CLASS_URL = reverse("private:private_classes-list")
  TUTOR_OFFER_URL = reverse("private:tutor_offers-list")
  SELECT_TUTOR_URL = reverse("private:select_tutor")

  def setUp(self):
    self.education_level = EducationLevelFactory()
    self.tutor_profile = ProfileFactory(user_type=UserType.TUTOR, education_level=self.education_level)
    self.student_profile1 = ProfileFactory(user_type=UserType.STUDENT, education_level=self.education_level)
    self.student_profile2 = ProfileFactory(user_type=UserType.STUDENT, education_level=self.education_level)
    self.subject = SubjectFactory(education_level=self.education_level)

    self.student_token = TokenFactory(user= self.student_profile1.user)
    self.tutor_token = TokenFactory(user = self.tutor_profile.user)
    
  def test_create_private_class(self):
    req = {
      "subject": self.subject.id,
      "education_level": self.education_level.id,
      "description": "A description",
      "rate": Decimal("0.00"),
    }

    expected_resp = {
      "student": self.student_profile1.id,
      "subject": self.subject.id,
      "education_level_name": self.education_level.name,
      "rate": "0.00",
    }

    resp = self.client.post(self.PRIVATE_CLASS_URL, data=req, HTTP_AUTHORIZATION=f"Token {self.student_token}")
    self.assertEqual(resp.status_code, 201)
    self.assertEqual(PrivateClass.objects.count(), 1)
    
    for key in expected_resp.keys():
      self.assertEqual(expected_resp[key], resp.json()[key])

  def test_private_class_offer_create(self):
    private_class = PrivateClassFactory(student=self.student_profile1, education_level=self.education_level)

    req = {
      "private_class" : private_class.id,
    }

    resp = self.client.post(self.TUTOR_OFFER_URL, data=req, HTTP_AUTHORIZATION=f"Token {self.tutor_token}")

    self.assertEqual(resp.status_code, 201)
    self.assertEqual(PrivateClassOffer.objects.count(), 1)
    self.assertEqual(PrivateClass.objects.last().privateclassoffer_set.count(), 1)

  def test_private_class_multiple_offers(self):
    private_class = PrivateClassFactory(student=self.student_profile1, education_level=self.education_level)
    tutor2 = ProfileFactory(user_type=UserType.TUTOR, education_level=self.education_level)
    tutor2_token = TokenFactory(user = tutor2.user)

    req = {
      "private_class" : private_class.id,
    }

    resp = self.client.post(self.TUTOR_OFFER_URL, data=req, HTTP_AUTHORIZATION=f"Token {self.tutor_token}")
    self.assertEqual(resp.status_code, 201)
    self.assertEqual(PrivateClassOffer.objects.count(), 1)
    self.assertEqual(PrivateClass.objects.last().privateclassoffer_set.count(), 1)

    resp = self.client.post(self.TUTOR_OFFER_URL, data=req, HTTP_AUTHORIZATION=f"Token {tutor2_token}")
    self.assertEqual(resp.status_code, 201)
    self.assertEqual(PrivateClassOffer.objects.count(), 2)
    self.assertEqual(PrivateClass.objects.last().privateclassoffer_set.count(), 2)
  
  def test_private_class_multiple_offers_same_user(self):
    private_class = PrivateClassFactory(student=self.student_profile1, education_level=self.education_level)
    req = {
      "private_class" : private_class.id,
    }
    resp = self.client.post(self.TUTOR_OFFER_URL, data=req, HTTP_AUTHORIZATION=f"Token {self.tutor_token}")
    self.assertEqual(resp.status_code, 201)
    self.assertEqual(PrivateClassOffer.objects.count(), 1)
    self.assertEqual(PrivateClass.objects.last().privateclassoffer_set.count(), 1)

    with self.assertRaises(IntegrityError):
      resp = self.client.post(self.TUTOR_OFFER_URL, data=req, HTTP_AUTHORIZATION=f"Token {self.tutor_token}")

  def test_select_tutor_private_class(self):
    private_class = PrivateClassFactory(student=self.student_profile1, education_level=self.education_level)
    tutor2 = ProfileFactory(user_type=UserType.TUTOR, education_level=self.education_level)
    tutor2_token = TokenFactory(user = tutor2.user)

    req = {
      "private_class" : private_class.id,
    }

    resp = self.client.post(self.TUTOR_OFFER_URL, data=req, HTTP_AUTHORIZATION=f"Token {self.tutor_token}")
    self.assertEqual(resp.status_code, 201)
    self.assertEqual(PrivateClassOffer.objects.count(), 1)
    self.assertEqual(PrivateClass.objects.last().privateclassoffer_set.count(), 1)

    resp = self.client.post(self.TUTOR_OFFER_URL, data=req, HTTP_AUTHORIZATION=f"Token {tutor2_token}")
    self.assertEqual(resp.status_code, 201)
    self.assertEqual(PrivateClassOffer.objects.count(), 2)
    self.assertEqual(PrivateClass.objects.last().privateclassoffer_set.count(), 2)

    self.assertEqual(PrivateClassOffer.objects.filter(status=PrivateClassOfferStatus.PENDING).count(), 2)

    req = {
      "private_class_id" : private_class.id,
      "tutor_id": tutor2.id,
    }

    resp = self.client.post(self.SELECT_TUTOR_URL, data=req, HTTP_AUTHORIZATION=f"Token {self.student_token}")
    self.assertEqual(resp.status_code, 200)

    self.assertEqual(PrivateClassOffer.objects.filter(status=PrivateClassOfferStatus.CANCELLED).count(), 1)
    self.assertEqual(PrivateClassOffer.objects.filter(status=PrivateClassOfferStatus.ACCEPTED).count(), 1)
    self.assertEqual(PrivateClass.objects.last().tutor.id, tutor2.id)
