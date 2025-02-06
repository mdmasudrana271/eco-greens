from django.db import models
from django.utils.text import slugify


# Create your models here.

class Categories(models.Model):
    name=models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"