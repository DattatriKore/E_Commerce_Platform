from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer 
from ProductAuth.models import Product

# Create your views here.

# Cart Management
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_admin or user.is_superuser:
            cart = Cart.objects.all()
        else:
            cart = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart,many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        cart, created = Cart.objects.get_or_create(user=request.user, product=Product.objects.get(id=product_id))
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart.quantity = quantity
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
        # cart_item, created = CartItem.objects.get_or_create(cart=cart)
        # cart_item.quantity = quantity
        # cart_item.save()
        # serializer = CartItemSerializer(cart_item)
        # return Response(serializer.data)

class CartUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self,request,pk):
        cart = Cart.objects.get(pk=pk)
        serializer = CartSerializer(cart,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        user = request.user
        if user.is_admin or user.is_superuser:
            cart = Cart.objects.get(pk=pk)
        else:
            cart = Cart.objects.filter(user=user)
        cart.delete()
        return Response({'delete':'Delete SuccessFully'}, status=status.HTTP_204_NO_CONTENT)
    
class CartItemView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        cartitem = CartItem.objects.all()
        serializer = CartItemSerializer(cartitem, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data
        cart_id = Cart.objects.get(id=data['cart'])
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart_id)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# class CartItemView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         cartitem = CartItem.objects.get()
#         serializer = CartItemSerializer(cartitem)
#         return Response(serializer.data)

#     def post(self,request):
#         def post(self,request):
#             cart_id = request.data.get('cart_id')
#             cartitem, created = CartItem.objects.get_or_create(cart=Cart.objects.get(id=cart_id))
#             quantity = request.data.get('quantity', 1)
#             cart = Cart.objects.get(id=cart_id)
#             cartitem.quantity = quantity
#             cartitem.save()
#             serializer = CartItemSerializer(cartitem)
#             return Response(serializer.data)
            
#     # def post(self, request):
#     #     product_id = request.data.get('product_id')
#     #     cart, created = Cart.objects.get_or_create(user=request.user, product=Product.objects.get(id=product_id))
#     #     quantity = request.data.get('quantity', 1)
#     #     product = Product.objects.get(id=product_id)
#     #     cart.quantity = quantity
#     #     cart.save()
#     #     serializer = CartSerializer(cart)
    
#     def delete(self, request):
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         product_id = request.data.get('product_id')
#         product = Product.objects.get(id=product_id)
#         cart_item = CartItem.objects.get(cart=cart, product=product)
#         cart_item.delete()
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
    

# def post(self,request):
#         quantity = request.data.get('quantity', 1)
#         cartitem, created = CartItem.objects.get_or_create()
#         cart, created = Cart.objects.get_or_create(cartitem=cartitem)
#         cart.quantity = quantity
#         cart.save()
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
