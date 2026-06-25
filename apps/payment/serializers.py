from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment

        fields = [
            "id",
            "booking",
            "amount",
            "status",
            "transaction_id",
            "authority",
            "created_at"
        ]

        read_only_fields = [
            "status",
            "transaction_id",
            "authority",
            "amount"
        ]