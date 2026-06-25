import pytest

from apps.account.serializers import (
    SendCodeSerializer
)

pytestmark = pytest.mark.django_db


def test_valid_phone():

    serializer = SendCodeSerializer(
        data={
            "phone_number": "09123456789"
        }
    )

    assert serializer.is_valid()


def test_invalid_phone():

    serializer = SendCodeSerializer(
        data={
            "phone_number": "123"
        }
    )

    assert serializer.is_valid() is False