# ==================== ADD LIBRARY AND PACKAGE ====================
from django.urls import path
from .views import (
    HotelCreateView,
    HotelListView,
    HotelDetailView,
    HotelUpdateView,
    HotelDeleteView
)

# ==================== URLS ====================
name_app = "hotel"

urlpatterns = [

    path("create/", HotelCreateView.as_view(), name="hotel-create"),

    path("", HotelListView.as_view(), name="hotel-list"),

    path("<int:pk>/", HotelDetailView.as_view(), name="hotel-detail"),

    path("<int:pk>/update/", HotelUpdateView.as_view(), name="hotel-update"),

    path("<int:pk>/delete/", HotelDeleteView.as_view(), name="hotel-delete"),
]