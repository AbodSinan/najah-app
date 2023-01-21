from django.urls import include

from authentication.urls import url_patterns as auth_urls
from booking.urls import url_patterns as booking_urls
from education.urls import api_router as education_router
from profile.urls import url_patterns as profile_urls
from private.urls import url_patterns as private_urls

"""najah URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from najah.webhooks import webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('education/', include((education_router.urls, "education"))),
    path('booking/', include((booking_urls, "booking"))),
    path("profile/", include((profile_urls, "profile"))),
    path('auth/', include((auth_urls, "auth"))),
    path('api-auth/' , include('rest_framework.urls')),
    path('private/', include((private_urls, "private"))),
    path('webhook', webhook, name="webhook")
]
