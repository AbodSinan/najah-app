from announcement.models import Announcement
from django.http import JsonResponse
from fcm_django.models import FCMDevice

def send_announcement(request, room_id):
    devices = FCMDevice.objects.filter(room_id=room_id)
    devices.send_message(title="Announcement", body="Hello, this is an announcement.")
    Announcement.objects.create()
    return JsonResponse({"message": "Announcement sent"})
