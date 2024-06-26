from django.urls import path
from . import views as auth_views

urlpatterns = [
    path("login/", auth_views.custom_login,name="login"),
    path("register/", auth_views.custom_register,name="register"),
    path("logout/", auth_views.custom_logout,name="logout"),
]