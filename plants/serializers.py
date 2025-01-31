from rest_framework import serializers
from . import models




class PlantSerializer(serializers.ModelSerializer):
    # category_name = serializers.SerializerMethodField() 
    category_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    mobile_no = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    class Meta:
        model = models.Plants
        fields = '__all__'
        # fields = ['id', 'name', 'price', 'description', 'image', 'created_at', 'stock', 'category', 'category_name','seller','seller_name','mobile_no']  # Include category_name


    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    def get_seller_name(self, obj):
        return obj.seller.user.username if obj.category else None
    def get_mobile_no(self, obj):
        return obj.seller.mobile_no if obj.category else None