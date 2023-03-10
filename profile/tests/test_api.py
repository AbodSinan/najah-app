from django.urls import reverse
from rest_framework.test import APITestCase

from education.tests.factories import EducationLevelFactory
from profile.tests.factories import ProfileFactory, UserFactory, TokenFactory

class ProfileTestCase(APITestCase):
  OWN_PROFILE_URL = reverse("profile:profile")
  def setUp(self):
    self.education_level = EducationLevelFactory(name="primary")
    self.user_1 = UserFactory(first_name="John Doe", email="JohnDoe@testing.com")
    self.user_2 = UserFactory(first_name="Jane Doe", email="JaneDoe@testing.com")
    self.profile_1 = ProfileFactory(age=15, user=self.user_1)
    self.profile_2 = ProfileFactory(age=17, user=self.user_2)

    self.token = TokenFactory(user = self.profile_1.user)
    self.client.force_authenticate(user=self.user_1, token = self.token)

  def test_retrieve_profile(self):
    resp = self.client.get(reverse("profile:get_profile", kwargs={"pk": self.profile_1.pk}))
    resp_data = resp.json()
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp_data["id"], self.profile_1.pk)
    self.assertEqual(resp_data["first_name"], "John Doe")

  def test_update_profile_profile_fields(self):
    req_data = {"age": 500, "description": "AM not gut","education_level": self.education_level.id}
    resp = self.client.put(self.OWN_PROFILE_URL, data=req_data)
    self.assertEqual(resp.status_code, 200)
    self.profile_1.refresh_from_db()

    self.assertEqual(self.profile_1.age, 500)
    self.assertEqual(self.profile_1.description, "AM not gut")
    self.assertEqual(self.profile_1.education_level, self.education_level)

  def test_update_profile_user_fields(self):
    req_data = {"last_name": "Doe Mama", "email": "doe@mama.com"}
    resp = self.client.put(self.OWN_PROFILE_URL, data=req_data)
    self.assertEqual(resp.status_code, 200)
    self.profile_1.refresh_from_db()

    self.assertEqual(self.profile_1.user.last_name, "Doe Mama")
    self.assertEqual(self.profile_1.user.email, "doe@mama.com")