from rest_framework import serializers
from .models import Cart, CartItem
from ProductAuth.serializers import ProductSerializer
from UserAuth.serializers import UserProfileSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user','product','quantity']

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'quantity']
