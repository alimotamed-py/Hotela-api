import pytest

from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_send_code():

    client = APIClient()

    response = client.post(
        "/api/account/send-code/",
        {
            "phone_number": "09123456789"
        }
    )

    assert response.status_code == 200