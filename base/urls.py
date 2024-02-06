from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.userLogin, name = 'login'),
    path("logout/",views.userLogout, name = 'logout'),
    path("register/",views.registerPage, name = 'register'),
    
    path("",views.home, name="home"),
    path("room/<str:pk>/" , views.room, name = "room"),
    path("user/<int:pk>/", views.userProfile, name = 'user'),
    path("user-update/",views.userUpdate, name = "user-update"),
    
    path("create-room/", views.createRoom, name = "create-room"),
    path("update-room/<int:pk>/", views.updateRoom, name = 'update-room'),
    path("delete-room/<int:pk>/", views.deleteRoom, name = 'delete-room'),
    path("delete-message/<int:pk>/", views.deleteMessage, name = 'delete-message'),
    
    path("topics/",views.topicPage, name = "topics"),
    path("activity/", views.activityPage, name = "activity"),
    
    path("follow/<int:pk>/", views.follow,name= "follow"),
    path("unfollow/<int:pk>/", views.unfollow,name= "unfollow"),
]
