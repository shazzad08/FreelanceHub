from django.db import models
from django.conf import settings


class FreelanceProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='freelancer_profile'
    )

    profile_image = models.ImageField(
        upload_to='freelancers/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    skills = models.CharField(
        max_length=300,
        blank=True,
        help_text='Separate skills with commas'
    )

    github = models.URLField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    portfolio = models.URLField(
        blank=True
    )

    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):

        return f"{self.user.first_name}   {self.user.email}"


class ClientProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    company_logo = models.ImageField(
        upload_to='clients/',
        blank=True,
        null=True
    )

    company_description = models.TextField(
        blank=True
    )

    company_website = models.URLField(
        blank=True
    )

    def __str__(self):

        return f"{self.user.first_name} {self.user.email}"