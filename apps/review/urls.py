from django.urls import path
from .views import (
    ReviewCreateView,
    HotelReviewListView,
    ReviewUpdateView,
    ReviewDeleteView
)

urlpatterns = [

    path(
        "create/",
        ReviewCreateView.as_view()
    ),

    path(
        "hotel/",
        HotelReviewListView.as_view()
    ),

    path(
        "<int:pk>/update/",
        ReviewUpdateView.as_view()
    ),

    path(
        "<int:pk>/delete/",
        ReviewDeleteView.as_view()
    ),
]