from django.db import models
from accounts.models import User


class Notification(models.Model):
    """Notifications for users"""

    TYPE_CHOICES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('SUCCESS', 'Success'),
        ('DANGER', 'Danger/Urgent'),
    ]

    CATEGORY_CHOICES = [
        ('REGISTRATION', 'Registration Status'),
        ('APPLICATION', 'Application Status'),
        ('REPORT', 'Report Reminder/Status'),
        ('EVALUATION', 'Evaluation Reminder/Status'),
        ('PLACEMENT', 'Internship Placement'),
        ('AT_RISK', 'At Risk Alert'),
        ('SYSTEM', 'System Notification'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='INFO')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='SYSTEM')
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True, help_text="URL to redirect when clicked")

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.title} → {self.recipient.email}"

    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    @classmethod
    def send_to_user(cls, user, title, message, notification_type='INFO', category='SYSTEM', link=''):
        """Helper method to create and send notification"""
        return cls.objects.create(
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            category=category,
            link=link
        )

    @classmethod
    def send_to_multiple(cls, users, title, message, notification_type='INFO', category='SYSTEM', link=''):
        """Send notification to multiple users"""
        notifications = [
            cls(
                recipient=user,
                title=title,
                message=message,
                notification_type=notification_type,
                category=category,
                link=link
            )
            for user in users
        ]
        return cls.objects.bulk_create(notifications)
