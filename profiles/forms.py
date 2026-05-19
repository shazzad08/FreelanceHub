from django import forms

from .models import (
    FreelanceProfile,
    ClientProfile
)

class FreelancerProfileForm(forms.ModelForm):
    
    class Meta:

        model = FreelanceProfile

        fields = [
            'profile_image',
            'bio',
            'skills',
            'github',
            'linkedin',
            'portfolio',
            'hourly_rate',
        ]
        
class ClientProfileForm(forms.ModelForm):
    
    class Meta:

        model = ClientProfile

        fields = [
            'company_name',
            'company_logo',
            'company_description',
            'company_website',
        ]