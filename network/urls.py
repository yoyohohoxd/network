
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("savepost/<int:id>/", views.savepost, name="savepost"),
    path("likepost/<int:id>/", views.likepost, name="likepost"),
    path("load_state/<int:id>", views.load_state, name="load_state"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("following/", views.following, name="following"),
    path("profile/<str:profile_username>/", views.profile, name="profile")
]
