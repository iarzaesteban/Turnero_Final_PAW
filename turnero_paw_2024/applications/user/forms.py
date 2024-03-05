from django import forms
from .models import Users

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = ['picture']

class LoginForm(forms.Form):
    usuario = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput)