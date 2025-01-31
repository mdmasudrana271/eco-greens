from rest_framework import serializers
from . import models
from plants.models import Plants




class OrderItemSerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source="plant.name", read_only=True)

    class Meta:
        model = models.OrderItem
        fields = ['id', 'plant', 'plant_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Order
        fields = ['id', 'user', 'total_price', 'status', 'order_date', 'updated_at', 'address', 'phone', 'order_items']
