from django import views
from rest_framework import viewsets, permissions

from education.models import EducationLevel, Subject, SubjectCategory
from education.serializers import SubjectCategorySerializer, SubjectSerializer, SubjectCategory, EducationLevelSerializer

class SubjectCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SubjectCategorySerializer
    queryset= SubjectCategory.objects.all()

class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SubjectSerializer
    queryset= Subject.objects.all()

class EducationLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EducationLevelSerializer
    queryset= EducationLevel.objects.all()
