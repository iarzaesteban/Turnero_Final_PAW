from django.core.exceptions import ValidationError
from django import forms
from .models import Users
from django.contrib.auth import authenticate
from applications.person.models import Person
from applications.state.models import State
class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=50)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.EmailField(label='Email')
    picture = forms.ImageField(label='Imagen', required=False)
    

class UserUpdateFooterForm(forms.Form):
    title = forms.CharField(label='Título', max_length=50)
    description = forms.CharField(label='Descripcion')
    link = forms.CharField(label='Ruta del Enlace', required=False)
    icon = forms.ImageField(label='Icono', required=False)
    icon_base64 = forms.CharField(label='icon_base64', required=False)
    
    
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
    repeat_new_password = forms.CharField(
                            label='Repetir Contraseña', 
                            required=True, 
                            widget=forms.PasswordInput(
                                        attrs={
                                            'placeholder': 'Repetir Contraseña'
                                            }))

class UpdatePictureForm(forms.Form):
    picture = forms.ImageField(label='Elija una fotografía', required=True)
    
class SendEmailForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', required=True)
    subject = forms.CharField(label='Asunto', max_length=100, required=True)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea, required=True)
    

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

class UpdateAttentionTimeUserForm(forms.Form):
    start_time_attention = forms.TimeField(
        label='Hora Inicio',
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time',
                                      'step': '1800'})
    )
    
    end_time_attention = forms.TimeField(
        label='Hora Fin',
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time', 
                                      'step': '1800'})
    )
    
    username = forms.CharField(widget=forms.HiddenInput(), required=False)