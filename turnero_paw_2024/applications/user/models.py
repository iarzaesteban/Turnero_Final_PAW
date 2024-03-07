from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
# Create your models here.


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    start_time_attention = models.DateField(null=True, blank=True)
    end_time_attention = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to='applications/user/user_pictures/', null=True, blank=True)
    code_verification = models.CharField(max_length=15, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username