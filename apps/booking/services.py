# ==================== ADD LIBRARY AND PACKAGE ====================
from apps.notification.tasks import create_notification
from .models import Notification
from django.utils.translation import gettext_lazy as _



def notify_booking_created(booking):

    create_notification(
        booking.customer.id,
        _("رزرو ثبت شد"),
        _("رزرو شما با موفقیت ثبت شد و در انتظار پرداخت است"),
        Notification.NotificationType.BOOKING
    )


def notify_payment_success(booking):

    create_notification(
        booking.customer.id,
        _("پرداخت موفق"),
        _("پرداخت شما با موفقیت انجام شد و رزرو تایید شد"),
        Notification.NotificationType.PAYMENT
    )