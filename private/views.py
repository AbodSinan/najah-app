from rest_framework import viewsets, views, status
from rest_framework.response import Response

from private.models import PrivateClass, PrivateClassOffer, PrivateClassStatus, PrivateClassOfferStatus
from private.serializers import ConfirmTutorSerializer, PrivateClassOfferSerializer, PrivateClassSerializer, StudentPrivateClassSerializer
from profile.models import Profile

# Create your views here.

class PrivateClassViewSet(viewsets.ModelViewSet):
  queryset = PrivateClass.objects.all()
  serializer_class = PrivateClassSerializer

  def perform_create(self, serializer):
    serializer.save(student=self.request.user.profile)

class StudentPrivateClassViewSet(viewsets.ModelViewSet):
  serializer_class = StudentPrivateClassSerializer

  def get_queryset(self):
    return PrivateClass.objects.filter(student=self.request.user.profile)

class TutorPrivateClassOfferViewSet(viewsets.ModelViewSet):
  serializer_class = PrivateClassOfferSerializer

  def get_queryset(self):
    return PrivateClassOffer.objects.filter(tutor=self.request.user.profile)
  
  def perform_create(self, serializer):
    serializer.save(tutor=self.request.user.profile)

class ConfirmPrivateClassTutorView(views.APIView):

  def post(self, request):
    serializer = ConfirmTutorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    private_class_id = serializer.data.get("private_class_id", None)

    try:
      private_class = PrivateClass.objects.get(id=private_class_id)
    except PrivateClass.DoesNotExist:
      return Response({"error": "Invalid private_class_id"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if self.request.user.profile.id != private_class.student.id:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    tutor_id = serializer.data.get("tutor_id", None)
    if not tutor_id or not PrivateClassOffer.objects.filter(private_class=private_class, tutor__id=tutor_id).exists():
      return Response({"error", "Invalid tutor_id"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    for class_offer in PrivateClassOffer.objects.filter(private_class=private_class).exclude(tutor__id=tutor_id):
      class_offer.status = PrivateClassOfferStatus.CANCELLED
      class_offer.save()

    accepted_offer = PrivateClassOffer.objects.get(private_class=private_class, tutor__id=tutor_id)
    accepted_offer.status = PrivateClassOfferStatus.ACCEPTED
    accepted_offer.save()

    private_class.tutor = Profile.objects.get(id=tutor_id)
    private_class.status = PrivateClassStatus.ONGOING
    private_class.save()

    return Response(status=status.HTTP_200_OK)
