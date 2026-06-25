# ==================== ADD LIBRARY AND PACKAGE ====================
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


# ==================== CITY MODEL ====================
class City(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("نام شهر")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("شهر")
        verbose_name_plural = _("شهرها")


# ==================== AMENITY MODEL ====================
class Amenity(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("امکانات")
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("امکانات")
        verbose_name_plural = _("امکانات")
        

# ==================== HOTEL MODEL ====================
class Hotel(models.Model):

    class HotelStatus(models.TextChoices):
        PENDING = "pending", _("در انتظار تایید")
        APPROVED = "approved", _("تایید شده")
        REJECTED = "rejected", _("رد شده")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hotels",
        verbose_name=_("مالک")
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("نام هتل")
    )

    description = models.TextField(
        verbose_name=_("توضیحات")
    )

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="hotels",
        verbose_name=_("شهر")
    )

    address = models.TextField(
        verbose_name=_("آدرس")
    )

    

    star = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name=_("ستاره")
    )

    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name="hotels",
        verbose_name=_("امکانات")
    )

    thumbnail = models.ImageField(
        upload_to="hotels/thumbnails/",
        blank=True,
        null=True
    )

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=HotelStatus.choices,
        default=HotelStatus.PENDING
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("هتل")
        verbose_name_plural = _("هتل ها")


# ==================== HOTEL IMAGE MODEL ====================
class HotelImage(models.Model):

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="hotels/gallery/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.hotel.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("تصویر هتل")
        verbose_name_plural = _("تصاویر هتل")


# ==================== HOTEL POLICY MODEL ====================
class HotelPolicy(models.Model):

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="policies"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("قانون هتل")
        verbose_name_plural = _("قوانین هتل")