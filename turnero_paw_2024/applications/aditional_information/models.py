from django.db import models

# Create your models here.

class AditionalInformation(models.Model):
    short_description = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title