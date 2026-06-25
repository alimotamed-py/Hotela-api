import pytest
from datetime import date, timedelta

from apps.booking.serializers import BookingSerializer
from apps.booking.models import Booking
from .factories import RoomFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_booking_serializer_valid():

    room = RoomFactory()

    data = {
        "room": room.id,
        "check_in": date.today() + timedelta(days=1),
        "check_out": date.today() + timedelta(days=3),
        "guests": 2
    }

    serializer = BookingSerializer(data=data)

    assert serializer.is_valid(), serializer.errors


def test_booking_overlap():

    room = RoomFactory()
    user = UserFactory()

    Booking.objects.create(
        customer=user,
        room=room,
        check_in=date.today() + timedelta(days=1),
        check_out=date.today() + timedelta(days=5),
        total_price=1000,
        status="confirmed"
    )

    data = {
        "room": room.id,
        "check_in": date.today() + timedelta(days=3),
        "check_out": date.today() + timedelta(days=7),
        "guests": 1
    }

    serializer = BookingSerializer(data=data)

    assert not serializer.is_valid()