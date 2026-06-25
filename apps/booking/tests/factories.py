import factory

from apps.account.models import CustomUser
from apps.hotel.models import Hotel, City
from apps.rooms.models import Room
from apps.booking.models import Booking


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomUser

    phone_number = factory.Sequence(
        lambda n: f"0912000{n:04d}"
    )

    role = "customer"


class OwnerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomUser

    phone_number = factory.Sequence(
        lambda n: f"0935000{n:04d}"
    )

    role = "owner"


class CityFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = City

    name = factory.Sequence(
        lambda n: f"City {n}"
    )


class HotelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Hotel

    owner = factory.SubFactory(OwnerFactory)

    city = factory.SubFactory(CityFactory)

    name = factory.Sequence(
        lambda n: f"Hotel {n}"
    )

    description = "Test Hotel"

    address = "Test Address"


class RoomFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Room

    hotel = factory.SubFactory(HotelFactory)

    title = "VIP Room"

    room_number = factory.Sequence(
        lambda n: f"{100+n}"
    )

    price_per_night = 100

    capacity = 2


class BookingFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Booking

    customer = factory.SubFactory(UserFactory)

    room = factory.SubFactory(RoomFactory)