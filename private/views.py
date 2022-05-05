from rest_framework import viewsets, views, status
from rest_framework.response import Response

from private.models import PrivateClass, PrivateClassOffer, PrivateClassStatus, PrivateClassOfferStatus
from private.serializers import PrivateClassOfferSerializer, PrivateClassSerializer, StudentPrivateClassSerializer
from profile.models import Profile

# Create your views here.

class PrivateClassViewSet(viewsets.ModelViewSet):
  queryset = PrivateClass.objects.all()
  serializer_class = PrivateClassSerializer

class StudentPrivateClassViewSet(viewsets.ModelViewSet):
  serializer_class = StudentPrivateClassSerializer

  def get_queryset(self):
    return PrivateClass.objects.filter(student=self.request.user.profile)

class TutorPrivateClassOfferViewSet(viewsets.ModelViewSet):
  serializer_class = PrivateClassOfferSerializer

  def get_queryset(self):
    return PrivateClassOffer.objects.filter(tutor=self.request.user.profile)

class ConfirmPrivateClassTutorView(views.APIView):

  def post(self, request):
    private_class_id = self.kwargs["private_class_od"]
    private_class = PrivateClass.objects.get(id=private_class_id)
    if self.request.user.profile is not private_class.student:
      return Response(status=status.HTTP_401_FORBIDDEN)
    
    tutor_id = request.data.get("tutor_id", None)
    if not tutor_id or not PrivateClassOffer.objects.filter(private_class=private_class, tutor__id=tutor_id).exists():
      return Response({"error", "Invalid tutor_id"}, status=status.HTTP_422_BAD_REQUEST)

    for class_offer in PrivateClassOffer.objects.filter(private_class=private_class).exclude(tutor__id=tutor_id):
      class_offer.status = PrivateClassOfferStatus.CANCELLED
      class_offer.save()

    accepted_offer = PrivateClassOffer.objects.get(private_class=private_class, tutor__id=tutor_id)
    accepted_offer.status = PrivateClassOfferStatus.ACCEPTED
    accepted_offer.save()

    private_class.tutor = Profile.objects.get(id=tutor_id)
    private_class.save()
