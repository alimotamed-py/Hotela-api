from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from drf_spectacular.utils import extend_schema

from .models import Room
from .serializers import RoomSerializer
from .permissions import IsHotelOwnerOrAdmin
from datetime import datetime

from django.db.models import Q
from rest_framework import generics

from .models import Room
from apps.booking.models import Booking
from .serializers import RoomSerializer



class RoomCreateView(generics.CreateAPIView):

    queryset = Room.objects.all()

    serializer_class = RoomSerializer

    permission_classes = [
        IsAuthenticated,
        IsHotelOwnerOrAdmin
    ]

    @extend_schema(tags=["Rooms"])
    def perform_create(self, serializer):

        hotel = serializer.validated_data["hotel"]

        if (
            hotel.owner != self.request.user
            and getattr(
                self.request.user,
                "role",
                None
            ) != "admin"
        ):
            raise PermissionDenied(
                "شما مالک این هتل نیستید"
            )

        serializer.save()


class RoomListView(generics.ListAPIView):

    serializer_class = RoomSerializer

    def get_queryset(self):

        hotel_id = self.request.query_params.get(
            "hotel"
        )

        queryset = Room.objects.filter(
            is_available=True,
            hotel__is_active=True,
            hotel__status="approved"
        ).select_related(
            "hotel"
        ).prefetch_related(
            "images",
            "amenities"
        )

        if hotel_id:
            queryset = queryset.filter(
                hotel_id=hotel_id
            )

        return queryset


class RoomDetailView(generics.RetrieveAPIView):

    serializer_class = RoomSerializer

    queryset = Room.objects.select_related(
        "hotel"
    ).prefetch_related(
        "images",
        "amenities"
    )


class RoomUpdateView(generics.UpdateAPIView):

    serializer_class = RoomSerializer

    permission_classes = [
        IsAuthenticated,
        IsHotelOwnerOrAdmin
    ]

    queryset = Room.objects.select_related(
        "hotel",
        "hotel__owner"
    )

    def perform_update(self, serializer):

        room = self.get_object()

        if (
            room.hotel.owner != self.request.user
            and getattr(
                self.request.user,
                "role",
                None
            ) != "admin"
        ):
            raise PermissionDenied(
                "اجازه ویرایش ندارید"
            )

        serializer.save()


class RoomDeleteView(generics.DestroyAPIView):

    queryset = Room.objects.select_related(
        "hotel",
        "hotel__owner"
    )

    serializer_class = RoomSerializer

    permission_classes = [
        IsAuthenticated,
        IsHotelOwnerOrAdmin
    ]
    
    
class AvailableRoomsView(generics.ListAPIView):

    serializer_class = RoomSerializer

    def get_queryset(self):

        check_in = self.request.query_params.get(
            "check_in"
        )

        check_out = self.request.query_params.get(
            "check_out"
        )

        hotel_id = self.request.query_params.get(
            "hotel"
        )

        queryset = Room.objects.filter(
            is_available=True,
            hotel__status="approved"
        )

        if hotel_id:
            queryset = queryset.filter(
                hotel_id=hotel_id
            )

        if not check_in or not check_out:
            return queryset

        booked_rooms = Booking.objects.filter(
            status__in=[
                Booking.BookingStatus.PENDING,
                Booking.BookingStatus.CONFIRMED
            ]
        ).filter(
            Q(check_in__lt=check_out) &
            Q(check_out__gt=check_in)
        ).values_list(
            "room_id",
            flat=True
        )

        return queryset.exclude(
            id__in=booked_rooms
        )