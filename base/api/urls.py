from django.urls import path
from . import views

urlpatterns = [
    path("",views.getRoutes),
    path("rooms", views.getRoom),
    path("rooms/<int:pk>",views.getRoomValue)
]
