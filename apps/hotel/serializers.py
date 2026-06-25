# ==================== ADD LIBRARY AND PACKAGE ====================
from rest_framework import serializers
from .models import Hotel, HotelImage


# ==================== HOTEL IMAGE ====================
class HotelImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelImage
        fields = ["id", "image"]


# ==================== HOTEL LIST & DETAIL ====================
class HotelSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.phone_number")

    city_name = serializers.CharField(source="city.name", read_only=True)

    amenities = serializers.StringRelatedField(many=True, read_only=True)

    images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "city",
            "city_name",
            "address",
            "star",
            "average_rating",
            "amenities",
            "is_active",
            "images",
            "created_at"
        ]


# ==================== HOTEL CREATE/UPDATE ====================
class HotelCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        exclude = [
            "owner",
            "average_rating",
            "status",
            "created_at",
            "updated_at"
        ]


# ==================== HOTEL IMAGE CREATE ====================
class HotelImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelImage
        fields = ["id", "hotel", "image"]