# ==================== ADD LIBRARY ====================
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.hotel.models import Hotel, Amenity


# ==================== ROOM MODEL ====================
class Room(models.Model):

    class RoomType(models.TextChoices):
        SINGLE = "single", _("تک نفره")
        DOUBLE = "double", _("دو نفره")
        TWIN = "twin", _("دو تخت جدا")
        SUITE = "suite", _("سوئیت")
        VIP = "vip", _("VIP")

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name=_("هتل")
    )

    title = models.CharField(
        max_length=255,
        verbose_name=_("عنوان اتاق")
    )

    room_number = models.CharField(
        max_length=50,
        verbose_name=_("شماره اتاق")
    )

    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
        default=RoomType.SINGLE
    )

    price_per_night = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("قیمت هر شب")
    )

    capacity = models.PositiveIntegerField(
    verbose_name=_("ظرفیت")
    )

    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name="rooms",
        verbose_name=_("امکانات اتاق")
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_number}"

    class Meta:
        verbose_name = _("اتاق")
        verbose_name_plural = _("اتاق‌ها")
        unique_together = ("hotel", "room_number")
        ordering = ["-created_at"]


# ==================== ROOM IMAGE ====================
class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="rooms/")

    def __str__(self):
        return f"Image - {self.room.room_number}"
    
    class Meta:
        verbose_name = _("تصویر اتاق")
        verbose_name_plural = _("تصاویر اتاق")


# ==================== ROOM AVAILABILITY (OPTIONAL ADVANCED) ====================
class RoomAvailability(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="availability"
    )

    date = models.DateField()

    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("room", "date")

        indexes = [
        models.Index(
            fields=["room", "date"]
        )
    ]