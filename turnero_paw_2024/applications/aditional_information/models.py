from django.db import models

class AditionalInformation(models.Model):
    short_description = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        """Convierte la instancia del modelo a un diccionario."""
        return {
            "short_description": self.short_description,
            "title": self.title,
            "description": self.description,
            "icon": self.icon,
            "link": self.link,
        }

    @classmethod
    def get_all_information(cls):
        """Obtén todas las instancias serializadas."""
        return [info.to_dict() for info in cls.objects.all()]

    def update_information(self, data):
        """Actualiza la instancia con los datos proporcionados."""
        self.title = data.get("title", self.title)
        self.description = data.get("description", self.description)
        self.link = data.get("link", self.link)
        self.icon = data.get("icon_base64", self.icon)
        self.save()

    def delete_information(self):
        """Elimina la instancia."""
        self.delete()

    def get_aditional_information():
        return AditionalInformation.objects.all()
    
    def create_aditional_information(form):
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        link = form.cleaned_data['link']
        icon_base64 = form.cleaned_data['icon_base64']            
        
        AditionalInformation.objects.create(
            title=title,
            description=description,
            link=link,
            icon=icon_base64
        )