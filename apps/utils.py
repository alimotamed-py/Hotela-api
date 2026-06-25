from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


def auth_client(user):
    client = APIClient()
    token = get_token(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client