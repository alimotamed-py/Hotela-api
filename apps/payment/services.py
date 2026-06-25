from apps.booking.models import Booking


def confirm_booking_payment(payment):

    booking = payment.booking

    booking.status = Booking.BookingStatus.CONFIRMED
    booking.save(update_fields=["status"])