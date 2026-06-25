import uuid


class PaymentGateway:

    @staticmethod
    def request_payment(amount):

        authority = str(uuid.uuid4())

        return {
            "authority": authority,
            "payment_url": f"https://payment-gateway.com/pay/{authority}"
        }

    @staticmethod
    def verify_payment(authority):

        return {
            "status": True,
            "transaction_id": str(uuid.uuid4())
        }