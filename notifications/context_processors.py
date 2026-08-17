from .models import Notification


def notifications(request):

    if request.user.is_authenticated:

        user_notifications = Notification.objects.filter(
            user=request.user
        )[:10]

        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        return {
            "user_notifications": user_notifications,
            "unread_notifications_count": unread_count,
        }

    return {
        "user_notifications": [],
        "unread_notifications_count": 0,
    }