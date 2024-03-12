from django.db import models
from applications.user.models import Users
# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"