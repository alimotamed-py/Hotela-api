# ==================== ADD LIBRARY AND PACKAGE ====================
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.rooms.models import Room


# ==================== BOOKING MODEL ====================
class Booking(models.Model):

    class BookingStatus(models.TextChoices):
        PENDING = "pending", _("در انتظار پرداخت")
        CONFIRMED = "confirmed", _("تایید شده")
        CANCELLED = "cancelled", _("لغو شده")
        COMPLETED = "completed", _("تکمیل شده")

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")

    check_in = models.DateField()
    check_out = models.DateField()

    guests = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.phone_number} - {self.room.room_number}"

    class Meta:
        verbose_name = _("رزرو")
        verbose_name_plural = _("رزروها")
        ordering = ["-created_at"]