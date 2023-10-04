from django.urls import path
from . import views
urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutPage, name="logout"),

    path("", views.home, name="home"),
    path("room/<int:id>/", views.room, name="room"),
    path("create-room/", views.creat_room, name="create-room"),
    path("update-room/<int:id>", views.update_room, name="update-room"),
    path("delete-room/<int:id>", views.delete_room, name="delete-room"),




]
