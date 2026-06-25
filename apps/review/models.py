# ==================== ADD LIBRARY ====================
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.hotel.models import Hotel


# ==================== REVIEW MODEL ====================
class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")
        unique_together = ("user", "hotel")
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["hotel", "rating"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.hotel.name} - {self.rating}"