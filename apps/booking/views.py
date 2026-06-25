# ==================== ADD LIBRARY AND PACKAGE ====================
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsCustomerOrAdmin, IsBookingOwnerOrAdmin
from apps.notification.services import notify_booking_created
from django.utils.translation import gettext_lazy as _



# ==================== CREATE BOOKING ====================
class BookingCreateView(generics.CreateAPIView):
    """
    Send a verification code to a user's phone number.\n
    POST /api/account/send-code/\n
    Permissions: AllowAny
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    permission_classes = [IsAuthenticated, IsCustomerOrAdmin]

    @extend_schema(tags=["Booking"])
    def perform_create(self, serializer):
        booking = serializer.save()
        notify_booking_created(booking)


# ==================== MY BOOKINGS ====================
class MyBookingListView(generics.ListAPIView):
    """
    Send a verification code to a user's phone number.\n
    POST /api/account/send-code/\n
    Permissions: AllowAny
    """

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(tags=['My Booking'])
    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user).select_related(
            "customer", "room", "room__hotel")


# ==================== BOOKING DETAIL ====================
class BookingDetailView(generics.RetrieveAPIView):
    """
    Send a verification code to a user's phone number.\n
    POST /api/account/send-code/\n
    Permissions: AllowAny
    """

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsBookingOwnerOrAdmin]
    
    @extend_schema(tags=['Booking Detail'])
    def get_queryset(self):
        if getattr(self.request.user, "role", None) == "admin":
            return Booking.objects.select_related("customer", "room", "room__hotel")
        return Booking.objects.filter(customer=self.request.user).select_related(
            "customer", "room", "room__hotel")


# ==================== CANCEL BOOKING ====================
class CancelBookingView(APIView):
    """
    Send a verification code to a user's phone number.\n
    POST /api/account/send-code/\n
    Permissions: AllowAny
    """

    permission_classes = [IsAuthenticated, IsBookingOwnerOrAdmin]

    @extend_schema(tags=['Cancel Booking'])
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        self.check_object_permissions(request, booking)

        if booking.status == Booking.BookingStatus.COMPLETED:
            raise ValidationError(_("رزرو تکمیل شده قابل لغو نیست"))

        if booking.status == Booking.BookingStatus.CANCELLED:
            raise ValidationError(_("این رزرو قبلاً لغو شده است"))
                
        booking.status = Booking.BookingStatus.CANCELLED
        booking.save(update_fields=["status"])

        return Response({"message": _("رزرو با موفقیت لغو شد")}, status=status.HTTP_200_OK)