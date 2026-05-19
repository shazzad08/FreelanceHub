from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

from .models import (
    FreelanceProfile,
    ClientProfile
)


#Auto Create Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        if instance.role == 'freelancer':

            FreelanceProfile.objects.create(
                user=instance
            )

        elif instance.role == 'client':

            ClientProfile.objects.create(
                user=instance
            )