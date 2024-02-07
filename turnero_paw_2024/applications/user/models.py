from django.db import models
from applications.person.models import Person
# Create your models here.


class Users(models.Model):
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    loggin = models.BooleanField(default=False)
    start_time_attention = models.DateField(null=True, blank=True)
    end_time_attention = models.DateField(null=True, blank=True)
    picture = models.BinaryField()

    def __str__(self):
        return self.username