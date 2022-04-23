from django.contrib.auth.models import User
from authentication.serializers import LoginSerializer, RegisterSerializer
from profile.serializers import ProfileSerializer

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CustomAuthToken(ObtainAuthToken):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        profile = ProfileSerializer(user.profile).data

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            **profile,
        })