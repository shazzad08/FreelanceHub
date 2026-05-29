from django import forms
from .models import Submission


class SubmissionForm(forms.ModelForm):

    class Meta:

        model = Submission

        fields = [

            'message',
            'file'

        ]

        widgets = {

            'message': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':4
                }
            )

        }