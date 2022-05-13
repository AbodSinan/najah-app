from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase

class TestRegister(APITestCase):
    REGISTER_URL = reverse("auth:register")
    LOGIN_URL = reverse("auth:login")
    ADMIN_LOGIN_URL = reverse("admin:login")

    def test_register_user_success(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password_2": "passwer1234",
            "user_type": "S",
        }

        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_register_no_user_type(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password_2": "passwer1234",
        }
        
        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('user_type' in resp.data)
        self.assertEqual(User.objects.count(), 0)

    def test_register_wrong_user_type(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password_2": "passwer1234",
            "user_type": "Z",
        }
        
        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('user_type' in resp.data)
        self.assertEqual(User.objects.count(), 0)

    def test_register_then_login(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password_2": "passwer1234",
            "user_type": "S",
        }

        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

        login_req = {
            "email": "Test@email.com",
            "password": "passwer1234",
        }

        resp = self.client.login(email=login_req["email"], password=login_req["password"])
        self.assertTrue(resp)

    def test_register_same_email(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "passwer1234",
            "password_2": "passwer1234",
            "user_type": "S",
        }

        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

        request = {
            "email" : "Test@email.com",
            "first_name": "Lang",
            "last_name": "wong",
            "password": "passwer1234",
            "password_2": "passwer1234",
            "user_type": "S",
        }
        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 400)
        self.assertTrue("email" in resp.json())

    def test_register_then_login_failed(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password_2": "passwer1234",
            "user_type": "S",
        }

        resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

        login_req = {
            "email": "Test@email.com",
            "password": "passwer12",
        }

        resp = self.client.login(username=login_req["email"], password=login_req["password"])
        
        self.assertFalse(resp)

    def test_api_auth_endpoint(self):
        request = {
            "email" : "Test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "JohnDoe69",
            "password": "passwer1234",
            "password_2": "passwer1234",
            "user_type": "S",
        }

        reg_resp = self.client.post(self.REGISTER_URL, data=request)
        self.assertEqual(reg_resp.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

        login_req = {
            "email": "Test@email.com",
            "password": "passwer1234",
        }

        resp = self.client.post(self.LOGIN_URL, data=login_req)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("token" in resp.json())

    def test_login_admin_superuser(self):
        """
        Create a superuser and login as an admin (Test needed because we use custom Auth Backend)
        """
        User.objects.create_superuser(username="admin", password="passwer1234", email="admin@testing.com")

        resp = self.client.login(username="admin", password= "passwer1234")

        self.assertTrue(resp)
