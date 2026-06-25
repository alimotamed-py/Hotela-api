from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Payment
from .serializers import PaymentSerializer
from .payment_gateway import PaymentGateway

from apps.booking.models import Booking
from .services import confirm_booking_payment


# ==================== CREATE PAYMENT ====================
class PaymentCreateView(generics.CreateAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        booking = get_object_or_404(
            Booking,
            id=request.data.get("booking"),
            customer=request.user
        )

        # جلوگیری از پرداخت تکراری
        if hasattr(booking, "payment") and booking.payment.status == "success":
            raise ValidationError("این رزرو قبلاً پرداخت شده است")

        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                "amount": booking.total_price
            }
        )

        result = PaymentGateway.request_payment(payment.amount)

        payment.authority = result["authority"]
        payment.status = Payment.PaymentStatus.PENDING
        payment.save(update_fields=["authority", "status"])

        return Response(
            {
                "payment_url": result["payment_url"],
                "authority": payment.authority
            },
            status=status.HTTP_200_OK
        )


# ==================== PAYMENT VERIFY ====================
class PaymentVerifyView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        authority = request.query_params.get("Authority")

        payment = get_object_or_404(
            Payment,
            authority=authority
        )

        result = PaymentGateway.verify_payment(authority)

        if result["status"]:

            payment.status = Payment.PaymentStatus.SUCCESS
            payment.transaction_id = result["transaction_id"]
            payment.save(update_fields=["status", "transaction_id"])

            confirm_booking_payment(payment)

            return Response(
                {"message": "پرداخت موفق بود"},
                status=status.HTTP_200_OK
            )

        payment.status = Payment.PaymentStatus.FAILED
        payment.save(update_fields=["status"])

        return Response(
            {"message": "پرداخت ناموفق بود"},
            status=status.HTTP_400_BAD_REQUEST
        )