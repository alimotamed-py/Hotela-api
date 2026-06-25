# ==================== ADD LIBRARY AND PACKAGE ====================
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Hotel
from .filters import HotelFilter
from .pagination import HotelPagination
from .permissions import IsOwnerOrAdmin
from .serializers import HotelSerializer, HotelCreateUpdateSerializer



# ==================== HOTEL CREATE ====================
class HotelCreateView(generics.CreateAPIView):
    serializer_class = HotelCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ==================== HOTEL LIST ====================
class HotelListView(generics.ListAPIView):

    serializer_class = HotelSerializer
    pagination_class = HotelPagination

    queryset = Hotel.objects.filter(
        is_active=True,
        status=Hotel.HotelStatus.APPROVED
    ).select_related(
        "owner",
        "city"
    ).prefetch_related(
        "images",
        "amenities"
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = HotelFilter

    search_fields = [
        "name",
        "city__name",
        "address"
    ]

    ordering_fields = [
        "star",
        "average_rating",
        "created_at"
    ]

    ordering = [
        "-created_at"
    ]


# ==================== HOTEL DETAIL ====================
class HotelDetailView(generics.RetrieveAPIView):

    serializer_class = HotelSerializer

    queryset = Hotel.objects.filter(
        is_active=True,
        status=Hotel.HotelStatus.APPROVED
    ).select_related(
        "owner",
        "city"
    ).prefetch_related(
        "images",
        "amenities"
    )


# ==================== HOTEL UPDATE ====================
class HotelUpdateView(generics.UpdateAPIView):

    serializer_class = HotelCreateUpdateSerializer

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrAdmin
    ]

    queryset = Hotel.objects.all()

    def get_queryset(self):

        if getattr(self.request.user, "role", None) == "admin":
            return Hotel.objects.all()

        return Hotel.objects.filter(
            owner=self.request.user
        )


# ==================== HOTEL DELETE ====================
class HotelDeleteView(generics.DestroyAPIView):

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrAdmin
    ]

    queryset = Hotel.objects.all()

    def get_queryset(self):

        if getattr(self.request.user, "role", None) == "admin":
            return Hotel.objects.all()

        return Hotel.objects.filter(
            owner=self.request.user
        )