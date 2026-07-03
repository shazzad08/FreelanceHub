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
            'cover_image',
            'bio',
            'skills',
            'category',
            'country',
            'availability',
            'languages',
            'experience',
            'github',
            'linkedin',
            'portfolio',
            'hourly_rate',
        ]

        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write a professional summary about yourself...'
            }),

            'skills': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Django, Python, React'
            }),

            'category': forms.SelectMultiple(attrs={
                'class': 'form-select d-none'
            }),

            'country': forms.Select(attrs={
                'class': 'form-select'
            }),

            'availability': forms.Select(attrs={
                'class': 'form-select'
            }),

            'languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'English, Bangla'
            }),

            'experience': forms.Select(attrs={
                'class': 'form-select'
            }),

            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username'
            }),

            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/username'
            }),

            'portfolio': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com'
            }),

            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '10'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Styling for image upload
        self.fields['profile_image'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['cover_image'].widget.attrs.update({
            'class': 'form-control'
        })


class ClientProfileForm(forms.ModelForm):

    class Meta:
        model = ClientProfile
        fields = [
            'company_name',
            'company_logo',
            'cover_image',
            'company_description',
            'company_website',
            'country',
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),

            'company_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your company'
            }),

            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://company.com'
            }),

            'country': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['company_logo'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['cover_image'].widget.attrs.update({
            'class': 'form-control'
        })