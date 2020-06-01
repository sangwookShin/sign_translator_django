from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name='index'),
    path("communication/", views.communication),
    path("RoomSetting/", views.RoomSetting),
    path("index/", views.index),
    path("translate/", views.sln_translate),
]