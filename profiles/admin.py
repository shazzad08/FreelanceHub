from django.contrib import admin

from .models import (
    FreelanceProfile,
    ClientProfile
)


@admin.register(FreelanceProfile)
class FreelanceProfileAdmin(admin.ModelAdmin):

    list_display = [
        'first_name',
        'email',
    ]

    def first_name(self, obj):

        return obj.user.first_name

    def email(self, obj):

        return obj.user.email


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):

    list_display = [
        'first_name',
        'email',
    ]

    def first_name(self, obj):

        return obj.user.first_name

    def email(self, obj):

        return obj.user.email