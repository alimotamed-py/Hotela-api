from django.urls import path
from .views import *

urlpatterns = [

    path(
        "",
        RoomListView.as_view(),
        name="room-list"
    ),

    path(
        "available/",
        AvailableRoomsView.as_view(),
        name="available-rooms"
    ),

    path(
        "create/",
        RoomCreateView.as_view(),
        name="room-create"
    ),

    path(
        "<int:pk>/",
        RoomDetailView.as_view(),
        name="room-detail"
    ),

    path(
        "<int:pk>/update/",
        RoomUpdateView.as_view(),
        name="room-update"
    ),

    path(
        "<int:pk>/delete/",
        RoomDeleteView.as_view(),
        name="room-delete"
    ),
]