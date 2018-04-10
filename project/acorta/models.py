from django.db import models

# Create your models here.

class Url(models.Model):
    url = models.URLField(unique=True)
    
    def __str__(self):
        return self.url
