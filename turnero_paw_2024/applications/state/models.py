from django.db import models

# Create your models here.

class State(models.Model):
    short_description = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.short_description
    
    def get_all_states():
        return State.objects.all()
    
    def get_cancel_shifts():
        return State.objects.get(short_description='cancelado')
    
    def get_complete_shifts():
        return State.objects.get(short_description='completado')