# -*- coding: utf-8 -*-
"""URL routes for authentication and users."""

from django.urls import path
from .views import LoginView, MeView, RefreshTokenView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("me/", MeView.as_view(), name="me"),
]
