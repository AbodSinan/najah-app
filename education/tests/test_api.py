from django.urls import reverse
from education.models import Subject

from rest_framework.test import APITestCase

from education.tests.factories import SubjectCategoryFactory, SubjectTagFactory, SubjectFactory, EducationLevelFactory
from profile.tests.factories import UserFactory, TokenFactory

class TestSubjectViewSet(APITestCase):
    SUBJECT_LIST_URL = reverse("education:subjects-list")
    def setUp(self):
        self.user = UserFactory(username="user1")
        self.token = TokenFactory(user = self.user)
        self.education_level = EducationLevelFactory(name="Elementary")
        self.subject_category = SubjectCategoryFactory(name="Elementary Subjects")
        self.subject_tag1 = SubjectTagFactory(name="Tag 1")
        self.subject_tag2 = SubjectTagFactory(name="Tag 2")
        self.subject_tag3 = SubjectTagFactory(name="Tag 3")

        self.subject1 = SubjectFactory(
            name="subject1",
            subject_category=self.subject_category,
            subject_tags=[self.subject_tag1, self.subject_tag2]
        )
        self.subject2 = SubjectFactory(
            name="subject2",
            subject_category=self.subject_category,
            subject_tags=[self.subject_tag2, self.subject_tag3]
        )
        self.client.force_authenticate(user = self.user, token=self.token)

    def test_subject_list(self):
        response = self.client.get(self.SUBJECT_LIST_URL)
        self.assertEqual(len(response.json()), 2)

    def test_create_subject(self):
        request_data = {
            "name": "subject new",
            "description": "Some subject",
            "subject_category": self.subject_category.id,
            "education_level": self.education_level.id,
            "subject_tags": [self.subject_tag1.id, self.subject_tag3.id],
        }
        response = self.client.post(self.SUBJECT_LIST_URL, data=request_data)
        self.assertEqual(response.status_code, 201)

        new_subject = Subject.objects.last()
        self.assertEqual(new_subject.name, "subject new")
        self.assertEqual(new_subject.subject_tags.count(), 2)
        self.assertEqual(new_subject.subject_category.id, self.subject_category.id)

    def test_create_subject_no_tags(self):
        request_data = {
            "name": "subject new",
            "description": "Some subject",
            "subject_category": self.subject_category.id,
            "education_level": self.education_level.id,
        }
        response = self.client.post(self.SUBJECT_LIST_URL, data=request_data)
        self.assertEqual(response.status_code, 201)

        new_subject = Subject.objects.last()
        self.assertEqual(new_subject.name, "subject new")
        self.assertEqual(new_subject.subject_tags.count(), 0)
        self.assertEqual(new_subject.subject_category.id, self.subject_category.id)

    def test_create_subject_no_category_fail(self):
        request_data = {
            "name": "subject new",
            "description": "Some subject",
            "education_level": self.education_level.id,
            "subject_tags": [self.subject_tag1.id, self.subject_tag3.id],
        }
        response = self.client.post(self.SUBJECT_LIST_URL, data=request_data)
        self.assertEqual(response.status_code, 400)
