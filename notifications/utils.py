from .models import Notification


def create_notification(
    user,
    title,
    message,
    url=""
):

    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        url=url
    )