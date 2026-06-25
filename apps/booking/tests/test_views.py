import pytest
from datetime import date, timedelta

from apps.booking.models import Booking
from .factories import UserFactory, RoomFactory
from ..utils import auth_client

pytestmark = pytest.mark.django_db


def test_create_booking():

    user = UserFactory()
    room = RoomFactory()

    client = auth_client(user)

    payload = {
        "room": room.id,
        "check_in": date.today() + timedelta(days=1),
        "check_out": date.today() + timedelta(days=3),
        "guests": 2
    }

    response = client.post(
        "/api/bookings/create/",
        payload,
        format="json"
    )

    assert response.status_code == 201
    assert Booking.objects.count() == 1

    booking = Booking.objects.first()
    assert booking.customer == user
    assert booking.room == room