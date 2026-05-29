from django.db import models
from django.conf import settings
from messaging.models import Conversation


class Notification(models.Model):

    TYPE_CHOICES = (

        ('proposal', 'Proposal'),
        ('message', 'Message'),

    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='proposal'
    )

    message = models.TextField()

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    redirect_url = models.CharField(
    max_length=255,
    blank=True,
    null=True
)

    def __str__(self):
        return self.message