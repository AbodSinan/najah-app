from rest_framework import routers

from education.views import SubjectViewSet, SubjectCategoryViewSet, EducationLevelViewSet

app_name = "education"

api_router = routers.DefaultRouter()
api_router.register(
    "subjects",
    SubjectViewSet,
    basename="subjects"
)
api_router.register(
    "education-levels",
    EducationLevelViewSet,
    basename="education_levels"
)
api_router.register(
    "subject-categories",
    SubjectCategoryViewSet,
    basename="subject_categories",
)
