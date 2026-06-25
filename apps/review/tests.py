import pytest

from apps.booking.tests.factories import (
    UserFactory,
    HotelFactory
)

from ..utils import auth_client

pytestmark = pytest.mark.django_db


def test_create_review():

    user = UserFactory()
    hotel = HotelFactory()

    client = auth_client(user)

    response = client.post(
        "/api/reviews/create/",
        {
            "hotel": hotel.id,
            "rating": 5,
            "comment": "excellent"
        },
        format="json"
    )

    assert response.status_code == 201

    assert hotel.reviews.count() == 1

    review = hotel.reviews.first()
    assert review.rating == 5