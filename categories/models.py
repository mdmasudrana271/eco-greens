from django.db import models


# Create your models here.

class Categories(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=120,unique=True)

    def __str__(self):
        return f"{self.name}"