from django.db import models
from django.conf import settings
from projects.models import Project


class Conversation(models.Model):

    project = models.ForeignKey(Project,on_delete=models.CASCADE)

    client = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='client_conversations')

    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='freelancer_conversations')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title}"
    
    
class Message(models.Model):
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    body = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.sender.email