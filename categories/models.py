from django.db import models
from django.utils.text import slugify


# Create your models here.

class Categories(models.Model):
    name=models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # ✅ Auto-generate slug only if it's not provided
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"