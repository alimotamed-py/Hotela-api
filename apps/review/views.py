from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer
from .permissions import (
    IsCustomerOrAdmin,
    IsReviewOwnerOrAdmin
)


# ==================== CREATE REVIEW ====================
class ReviewCreateView(generics.CreateAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated,
        IsCustomerOrAdmin
    ]

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ==================== HOTEL REVIEWS LIST ====================
class HotelReviewListView(generics.ListAPIView):

    serializer_class = ReviewSerializer

    def get_queryset(self):

        hotel_id = self.request.query_params.get(
            "hotel"
        )

        if not hotel_id:
            return Review.objects.none()

        return Review.objects.filter(
            hotel_id=hotel_id
        ).select_related(
            "user",
            "hotel"
        ).order_by("-created_at")


# ==================== UPDATE REVIEW ====================
class ReviewUpdateView(generics.UpdateAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated,
        IsReviewOwnerOrAdmin
    ]


# ==================== DELETE REVIEW ====================
class ReviewDeleteView(generics.DestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated,
        IsReviewOwnerOrAdmin
    ]

    def perform_destroy(self, instance):

        hotel = instance.hotel
        instance.delete()

        # update rating after delete
        from .serializers import ReviewSerializer
        ReviewSerializer().update_hotel_rating(hotel)