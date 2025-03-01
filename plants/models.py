from django.db import models

from categories.models import Categories
from userprofile.models import UserProfile

# Create your models here.


class Plants(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    # img = models.ImageField(upload_to="plants/", null=True, blank=True)
    img=models.URLField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller', null=True, blank=True)

    def __str__(self):
        return self.name
    






class Blog(models.Model):
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='author',null=True, blank=True)
    img = models.URLField(max_length=100,null=True, blank=True)
