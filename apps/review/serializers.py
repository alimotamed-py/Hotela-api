from django.db.models import Avg
from rest_framework import serializers

from .models import Review
from apps.hotel.models import Hotel


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(
        source="user.phone_number"
    )

    class Meta:
        model = Review

        fields = [
            "id",
            "user",
            "hotel",
            "rating",
            "comment",
            "created_at"
        ]

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "امتیاز باید بین 1 تا 5 باشد"
            )

        return value

    def validate(self, data):

        user = self.context["request"].user
        hotel = data.get("hotel")

        if self.instance is None:  # فقط برای CREATE

            if Review.objects.filter(
                user=user,
                hotel=hotel
            ).exists():

                raise serializers.ValidationError(
                    "شما قبلاً برای این هتل نظر ثبت کرده‌اید"
                )

        return data

    def update_hotel_rating(self, hotel):

        avg = Review.objects.filter(
            hotel=hotel
        ).aggregate(
            avg=Avg("rating")
        )["avg"] or 0

        hotel.average_rating = round(avg, 2)
        hotel.save(
            update_fields=["average_rating"]
        )

    def create(self, validated_data):

        user = self.context["request"].user
        hotel = validated_data["hotel"]

        review = Review.objects.create(
            user=user,
            **validated_data
        )

        self.update_hotel_rating(hotel)

        return review

    def update(self, instance, validated_data):

        instance.rating = validated_data.get(
            "rating",
            instance.rating
        )

        instance.comment = validated_data.get(
            "comment",
            instance.comment
        )

        instance.save()

        self.update_hotel_rating(instance.hotel)

        return instance