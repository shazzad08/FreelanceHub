from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = [
            'category',
            'title',
            'description',
            'budget',
            'deadline'
        ]

        widgets = {

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter project title'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Describe your project'
                }
            ),

            'budget': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Budget amount'
                }
            ),

            'deadline': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }