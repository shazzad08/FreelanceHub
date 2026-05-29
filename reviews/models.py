from django.db import models
from django.conf import settings
from projects.models import Project


class Review(models.Model):

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )

    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )

    rating = models.IntegerField()

    feedback = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f'{self.freelancer}  {self.rating}'
        )