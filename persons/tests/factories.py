import factory

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user {}".format(n))
    class Meta:
        model = User

class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token