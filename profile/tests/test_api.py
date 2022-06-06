from django.urls import reverse
from rest_framework.test import APITestCase

from profile.tests.factories import ProfileFactory, UserFactory, TokenFactory

class ProfileTestCase(APITestCase):
  def setUp(self):
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
