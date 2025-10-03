from notifications.models import Notification


def notifications(request):
    """Add notifications to context"""
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

        recent_notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by('-created_at')[:5]

        return {
            'unread_notifications_count': unread_notifications,
            'recent_notifications': recent_notifications,
        }

    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }
