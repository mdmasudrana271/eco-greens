from rest_framework import serializers
from . import models




class PlantSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    mobile_no = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=models.Categories.objects.all())
    class Meta:
        model = models.Plants
        fields = '__all__'


    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    def get_seller_name(self, obj):
        return obj.seller.user.username if obj.seller else None

    def get_mobile_no(self, obj):
        return obj.seller.mobile_no if obj.seller else None
