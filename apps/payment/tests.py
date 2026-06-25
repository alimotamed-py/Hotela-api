import pytest
from datetime import date, timedelta

from apps.booking.models import Booking
from apps.booking.tests.factories import UserFactory, RoomFactory
from ..utils import auth_client

pytestmark = pytest.mark.django_db


def test_create_payment():

    user = UserFactory()
    room = RoomFactory()

    booking = Booking.objects.create(
        customer=user,
        room=room,
        check_in=date.today() + timedelta(days=1),
        check_out=date.today() + timedelta(days=2),
        total_price=500,
        status="pending"
    )

    client = auth_client(user)

    response = client.post(
        "/api/payments/create/",
        {"booking": booking.id},
        format="json"
    )

    assert response.status_code == 200

    booking.refresh_from_db()

    assert booking.payment is not None
    assert booking.payment.authority is not None
    assert booking.payment.amount == booking.total_price