from django.urls import path

from authentication.views import RegisterView, CustomAuthToken

app_name = "authentication"


url_patterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", CustomAuthToken.as_view(), name="login" )
]