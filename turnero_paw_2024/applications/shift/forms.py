from django import forms
from django.core.validators import MaxLengthValidator

class CancelShiftForm(forms.Form):
    verification_code = forms.CharField(max_length=6, required=False)
    cancel_description = forms.CharField(
        max_length=200,
        required=False,
        validators=[MaxLengthValidator(200)],
        widget=forms.Textarea(attrs={
            'id': 'cancel-description',
            'rows': 4,
            'cols': 50,
            'placeholder': 'Agrega una descripción...'
        })
    )

    def clean_cancel_description(self):
        verification_code = self.cleaned_data.get('verification_code', '')
        cancel_description = self.cleaned_data.get('cancel_description', '')
        if verification_code is not None and verification_code.strip() != "":
            return
        
        return cancel_description