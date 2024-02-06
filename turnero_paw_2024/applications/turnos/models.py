from django.db import models

# Create your models here.

class Turno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    fecha_turno = models.DateTimeField(auto_now_add=True)