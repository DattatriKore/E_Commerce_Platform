from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import Order
from UserAuth.models import User
from .serializers import  OrderSerializer
from Cart.models import Cart, CartItem
from django.conf import settings

# Create your views here.

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if user.is_admin or user.is_superuser:
            order = Order.objects.all()
        else:
            order = Order.objects.filter(user=user)
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            cart = self.request.data['cart']
            cart = Cart.objects.get(id=cart, user=request.user)
        except:
            return Response({'error':'Record not found'})
        print('Cart:',cart)
        price = cart.product.price
        print('Price:', price)
        quantity = cart.quantity
        print('Quantity:', quantity)
        total_price = price * quantity 
        print("Product:",cart.product)
        order = Order.objects.create(products=cart.product, user=cart.user, total_price=total_price,quantity=quantity)
        print(order)
        # for item in cart:
        #     Order.objects.create(order=order, products=item.product, quantity=item.quantity)
        # cart.delete()
        serializer = OrderSerializer(order)
        # send_mail(
        #     'Order Confirmation',
        #     f'Your order {order.id} has been placed successfully.',
        #     settings.EMAIL_HOST_USER,
        #     ['dattatri.kore@pcpl.io'],
        #     fail_silently=False,
        # )
        send_mail(
            subject='Order Confirmation',
            message=f'Thank you for your order! Your total amount is: {total_price}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    
