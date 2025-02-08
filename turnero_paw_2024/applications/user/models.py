import datetime
from PIL import Image
from io import BytesIO
from app.settings.base import EMAIL_HOST_USER
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from applications.person.models import Person

from .managers import UserManager
from .helpers import generate_confirmation_code

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    start_time_attention = models.TimeField(null=True, blank=True)
    end_time_attention = models.TimeField(null=True, blank=True)
    picture = models.BinaryField(null=True, blank=True)
    code_verification = models.CharField(max_length=15, blank=True)
    has_set_attention_times = models.BooleanField(default=False)
    has_default_password = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username   

    def retrieve_image(self):
        """Devuelve la imagen de perfil en formato PIL.Image."""
        if self.picture:
            return Image.open(BytesIO(self.picture))
        return None
    

    def authenticate_and_login_user(request, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return user


    def create_user(form_data):
        """Crea un usuario y una persona asociados."""
        # Validar contraseñas
        password = form_data.get('password')
        confirm_password = form_data.get('confirm_password')
        if password != confirm_password:
            raise ValueError('Las contraseñas no coinciden')

        # Validar username y email
        username = form_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise ValueError('El usuario ingresado ya está en uso')
        
        email = form_data.get('email')
        if Person.person_exists(email):
            raise ValueError('Este correo electrónico ya está en uso')

        # Procesar imagen
        picture = form_data.get('picture')
        output = BytesIO()
        if picture:
            img = Image.open(picture)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output, format='JPEG', quality=70)

        # Crear usuario
        verification_code = generate_confirmation_code()
        user = Users.objects.create_user(
            username=username,
            password=password,
            code_verification=verification_code,
            picture=output.getvalue()
        )

        # Crear persona
        person = {
            "first_name": form_data.get('first_name'),
            "last_name": form_data.get('last_name'),
            "email": email,
            "id_user": user

        }
        person = Person.create_person(person)

        return user, person


    def send_verification_email(user, person, current_user=None):
        """Envía un correo electrónico con el código de verificación."""
        date = datetime.datetime.now()
        date_str = date.strftime('%d-%m-%Y %H:%M')
        asunto = "Confirmación de correo"
        message = (
            f"El código de verificación es {user.code_verification}. "
            f"La hora es {date_str}."
        )
        recipient = [person.email] if current_user else [person.email, EMAIL_HOST_USER]
        send_mail(asunto, message, EMAIL_HOST_USER, recipient)


    def active_user(id):
        Users.objects.filter(id=id).update(is_active=True)


    def get_reset_users_actives(exclude_user):
        return  Users.objects.exclude(
                    username=exclude_user.username
                ).exclude(
                    start_time_attention__isnull=True
                ).exclude(
                    end_time_attention__isnull=True
                )

    def autenticate_user(user, password):
        return authenticate(username=user.username,
                                password=password)


    def change_user_password(user, new_password):
        user.set_password(new_password)
        if not user.has_default_password:
            user.has_default_password = True
        user.save()


    def user_have_set_attentions_time(user):
        return user.has_set_attention_times


    def user_has_attentions_time_different(user, start_time, end_time):
        return user.start_time_attention == start_time and user.end_time_attention == end_time


    def set_attentions_times_user(user, start_time, end_time):
        user.has_set_attention_times = True
        user.start_time_attention = start_time
        user.end_time_attention = end_time
        user.save()
