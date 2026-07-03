from django.db import models
from django.conf import settings
from categories.models import Category
from django_countries.fields import CountryField


class FreelanceProfile(models.Model):

    AVAILABILITY_CHOICES = [
        ('full_time', 'Full Time (40+ hrs/week)'),
        ('part_time', 'Part Time (10–30 hrs/week)'),
        ('less_than_10', 'Less than 10 hrs/week'),
        ('as_needed', 'As Needed'),
    ]

    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher (0-1 year)'),
        ('junior', 'Junior (1-2 years)'),
        ('mid', 'Intermediate (2-5 years)'),
        ('senior', 'Senior (5+ years)'),
        ('expert', 'Expert (10+ years)'),
    ]

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

    cover_image = models.ImageField(
        upload_to='freelancers/covers/',
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    skills = models.CharField(
        max_length=300,
        blank=True,
        help_text='Separate skills with commas'
    )

    category = models.ManyToManyField(Category, blank=True, related_name='freelancers')

    
    country = CountryField(blank=True)

    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        blank=True
    )

    languages = models.CharField(
        max_length=200,
        blank=True,
        help_text='Example: English, Bangla'
    )

    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        blank=True
    )

    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.email}"


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

    cover_image = models.ImageField(
        upload_to='clients/covers/',
        blank=True,
        null=True
    )

    company_description = models.TextField(blank=True)

    company_website = models.URLField(blank=True)

    country = CountryField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.email}"