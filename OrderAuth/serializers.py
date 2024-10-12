from rest_framework import serializers
from .models import Order
from ProductAuth.serializers import ProductSerializer
from UserAuth.serializers import UserProfileSerializer
        
# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['id','order','product','quantity']
        
class OrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    products = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id','user','products','total_price','quantity','created_at']