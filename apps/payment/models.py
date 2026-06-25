# ==================== ADD LIBRARY ====================
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.booking.models import Booking


# ==================== PAYMENT MODEL ====================
class Payment(models.Model):

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", _("در انتظار پرداخت")
        SUCCESS = "success", _("موفق")
        FAILED = "failed", _("ناموفق")
        REFUNDED = "refunded", _("برگشت داده شده")

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    authority = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.id} - {self.status}"

    class Meta:
        verbose_name = _("پرداخت")
        verbose_name_plural = _("پرداخت‌ها")
        indexes = [
            models.Index(fields=["authority"]),
            models.Index(fields=["status"]),
        ]