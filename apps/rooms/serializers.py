from rest_framework import serializers
from .models import Room, RoomImage


class RoomImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomImage
        fields = [
            "id",
            "image"
        ]


class RoomSerializer(serializers.ModelSerializer):

    hotel_name = serializers.CharField(
        source="hotel.name",
        read_only=True
    )

    amenities = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    images = RoomImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Room

        fields = [
            "id",
            "hotel",
            "hotel_name",
            "title",
            "room_number",
            "room_type",
            "price_per_night",
            "capacity",
            "amenities",
            "is_available",
            "images",
            "created_at"
        ]