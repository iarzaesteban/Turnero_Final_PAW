from django import forms
from .models import Users
from django.contrib.auth import authenticate


class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(
                        label='Contraseña', 
                        required=True, 
                        widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': 'Contraseña'
                                        }))
    confirm_password = forms.CharField(
                        label='Contraseña', 
                        required=True, 
                        widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': 'Repetir Contraseña'
                                        }))
    class Meta:
        model = Users
        fields = (
            'username',
            'picture',
            'start_time_attention',
            'end_time_attention'
        )

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('username', 'Las contraseñas no coinciden')

class LoginForm(forms.Form):
    username = forms.CharField(
                            label='Usuario', 
                            required=True, 
                            widget=forms.TextInput(
                                        attrs={
                                            'placeholder': 'Usuario'
                                            }))
    password = forms.CharField(
                            label='Contraseña', 
                            required=True, 
                            widget=forms.PasswordInput(
                                        attrs={
                                            'placeholder': 'Contraseña'
                                            }))
   
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Usuario o contraseña incorrectos")
        return self.cleaned_data


class UpdatePasswordForm(forms.Form):
    current_password = forms.CharField(
                            label='Contraseña Actual', 
                            required=True, 
                            widget=forms.PasswordInput(
                                        attrs={
                                            'placeholder': 'Contraseña Actual'
                                            }))
    new_password = forms.CharField(
                            label='Contraseña Nueva', 
                            required=True, 
                            widget=forms.PasswordInput(
                                        attrs={
                                            'placeholder': 'Contraseña Nueva'
                                            }))
   


class VerificationForm(forms.Form):
    code_verification = forms.CharField(required=True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_code_verification(self):
        code = self.cleaned_data['code_verification']

        if len(code) == 15:
            active = Users.objects.code_verification(self.id_user, code)
            if not active:
                raise forms.ValidationError("El codigo ingresado es incorrecto")
        else:
            raise forms.ValidationError("El codigo ingresado es incorrecto")