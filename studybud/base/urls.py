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
    
    path("delete-message/<int:id>", views.delete_message, name="delete-message"),

    path("user-profile/<int:id>", views.userProfile, name = "user-profile" ),
    path("update-profile/", views.updateUser, name = "update-user" ),

    path("topics/", views.topicsPage, name = "topics" ),
    path("activity/", views.activityPage, name = "activity" ),



]
