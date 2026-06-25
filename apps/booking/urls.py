# ==================== ADD LIBRARY AND PACKAGE ====================
from django.urls import path
from .views import (
    BookingCreateView,
    MyBookingListView,
    BookingDetailView,
    CancelBookingView
)

# ==================== URLS ====================
app_name = "booking"

urlpatterns = [

    path("create/", BookingCreateView.as_view(), name="booking-create"),

    path("my-bookings/", MyBookingListView.as_view(), name="my-bookings"),

    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),

    path("<int:pk>/cancel/", CancelBookingView.as_view(), name="booking-cancel"),
]