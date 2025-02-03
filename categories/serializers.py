from rest_framework import serializers
from .models import Categories
from django.utils.text import slugify

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=["id","name","slug"]

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["name"]) 
        return super().create(validated_data)