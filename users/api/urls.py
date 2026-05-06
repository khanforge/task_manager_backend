from django.urls import path
from .views import RegisterView, Login

urlpatterns = [
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", Login.as_view(), name="login")
]
