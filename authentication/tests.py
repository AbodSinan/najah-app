from django.urls import reverse

from rest_framework.test import APITestCase

from authentication.models import CustomUser

class TestRegister(APITestCase):
    REGISTER_URL = reverse("auth:register")

    def test_register_user_success(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password2": "passwer1234",
            "user_type": "S",
        }

        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_register_no_user_type(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password2": "passwer1234",
        }
        
        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('user_type' in resp.data)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_register_wrong_user_type(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password2": "passwer1234",
            "user_type": "Z",
        }
        
        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('user_type' in resp.data)
        self.assertEqual(CustomUser.objects.count(), 0)

