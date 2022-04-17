from rest_framework import routers

from education.views import SubjectViewSet

app_name = "education"

api_router = routers.DefaultRouter()
api_router.register(
    "subjects",
    SubjectViewSet,
    basename="subjects"
)
