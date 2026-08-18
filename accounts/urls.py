from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("register/", views.register_view,name="register"),
    path( "login/", LoginView.as_view( template_name="accounts/login.html" ), name="login" ),
    path( "logout/", LogoutView.as_view(), name="logout"),
    path( "profile/", views.profile, name="profile"),
    path( "profile/edit/", views.profile_edit, name="profile_edit"),
    path( "profile/password/",views.change_password, name="change_password"),

    ]