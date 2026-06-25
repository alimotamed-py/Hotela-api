from .models import Notification
from .tasks import create_notification


def notify_booking_created(booking):

    create_notification(
        booking.customer.id,
        "رزرو ثبت شد",
        "رزرو شما با موفقیت ثبت شد و در انتظار پرداخت است",
        Notification.NotificationType.BOOKING
    )


def notify_payment_success(booking):

    create_notification(
        booking.customer.id,
        "پرداخت موفق",
        "پرداخت شما با موفقیت انجام شد و رزرو تایید شد",
        Notification.NotificationType.PAYMENT
    )