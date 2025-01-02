from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import user_registration_view, logout, login

urlpatterns = [
    path("api/register/", user_registration_view, name="register"),
    path("api/token/", login, name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", logout, name="logout"),
]
