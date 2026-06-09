from django import forms
from .models import Proposal


class ProposalForm(forms.ModelForm):

    class Meta:
        model = Proposal

        fields = [
            'cover_letter',
            'bid_amount'
        ]

        widgets = {

            'cover_letter': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 8,
                    'placeholder': (
                        'Introduce yourself, explain your experience, '
                        'and describe how you will complete this project...'
                    )
                }
            ),

            'bid_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your bid amount'
                }
            )

        }