from django.urls import path
from .views import send_announcement

urlpatterns = [
    path('announcement/<str:room_id>/', send_announcement, name='send_announcement')
]
