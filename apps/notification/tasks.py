from apps.notification.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


def create_notification(
    user_id,
    title,
    message,
    type="system"
):

    try:
        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:
        return

    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=type
    )