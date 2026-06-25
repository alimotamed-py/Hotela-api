from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        BOOKING = "booking", _("رزرو")
        PAYMENT = "payment", _("پرداخت")
        SYSTEM = "system", _("سیستمی")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
            fields=["user", "is_read"]
            ),
        ]

        verbose_name = _("اعلان")
        verbose_name_plural = _("اعلان‌ها")