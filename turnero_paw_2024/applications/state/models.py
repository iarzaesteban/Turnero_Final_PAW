from django.db import models

# Create your models here.

class State(models.Model):
    short_description = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.short_description