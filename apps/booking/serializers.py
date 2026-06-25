# ==================== ADD LIBRARY AND PACKAGE ====================
from datetime import date
from django.db.models import Q
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Booking
from .utils import calculate_nights, calculate_price


# ==================== BOOKING SERIALIZER ====================
class BookingSerializer(serializers.ModelSerializer):

    customer = serializers.ReadOnlyField(source="customer.phone_number")

    total_price = serializers.ReadOnlyField()

    status = serializers.ReadOnlyField()

    class Meta:
        model = Booking

        fields = [
            "id",
            "customer",
            "room",
            "check_in",
            "check_out",
            "guests",
            "total_price",
            "status",
            "created_at"
        ]

    def validate(self, data):

        room = data["room"]
        check_in = data["check_in"]
        check_out = data["check_out"]

        if not room.is_available:
            raise serializers.ValidationError(_("این اتاق در حال حاضر غیرفعال است"))

        if check_in >= check_out:
            raise serializers.ValidationError(_("تاریخ ورود و خروج نامعتبر است"))

        if check_in < date.today():
            raise serializers.ValidationError(_("رزرو برای تاریخ گذشته امکان پذیر نیست"))

        if data["guests"] > room.capacity:
            raise serializers.ValidationError(_(f"ظرفیت این اتاق {room.capacity} نفر است"))

        overlap = Booking.objects.filter(room=room, status__in=[
                Booking.BookingStatus.PENDING,
                Booking.BookingStatus.CONFIRMED])

        if self.instance:
            overlap = overlap.exclude(pk=self.instance.pk)

        overlap = overlap.filter(Q(check_in__lt=check_out) & Q(check_out__gt=check_in)).exists()

        if overlap:
            raise serializers.ValidationError(_("این اتاق در بازه انتخابی رزرو شده است"))
                
        return data

    def create(self, validated_data):

        room = validated_data["room"]

        nights = calculate_nights(validated_data["check_in"], validated_data["check_out"])

        total_price = calculate_price(room.price_per_night, nights)

        return Booking.objects.create(customer=self.context["request"].user,
                                       total_price=total_price, **validated_data)