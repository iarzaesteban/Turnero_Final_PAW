from django.db import models
from applications.person.models import Person
from applications.user.models import Users
from applications.state.models import State

# Create your models here.

class Shift(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    id_state = models.ForeignKey(State, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=50)
    confirmation_url = models.URLField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} {self.hour} - {self.id_person}"