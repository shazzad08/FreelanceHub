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
                    'rows': 5
                }
            ),

            'bid_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }