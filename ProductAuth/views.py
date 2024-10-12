from django.shortcuts import render
from .models import Categories,Brand,Product
from .serializers import CategoriesSerializer,BrandSerializer,ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from UserAuth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .permissions import *
from rest_framework.permissions import BasePermission

# Create your views here.

# Category Management
class CategoriesListCreateView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]  
        elif self.request.method == 'POST':
            return [IsAdminorSuperuser()]  
        return super().get_permissions()
    
    def get(self,request):
        category = Categories.objects.all()
        serializer = CategoriesSerializer(category,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        user = request.user
        if user.is_admin or user.is_superuser:
            serializer = CategoriesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        
class CategoryPostRetrieveUpdateDeleteView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]  
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminorSuperuser()]  
        return super().get_permissions()
    
    def get(self,request,pk):
        category = Categories.objects.get(pk=pk)
        serializer = CategoriesSerializer(category)
        return Response(serializer.data)
    
    def put(self,request,pk):
        user = request.user
        if user.is_admin or user.is_superuser:
            category = Categories.objects.get(pk=pk)
            serializer = CategoriesSerializer(category,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
    
    def delete(self,request,pk):
        user = request.user
        if user.is_admin or user.is_superuser:
            category = Categories.objects.get(pk=pk)
            category.delete()
            return Response({'massage':'Delete SuccessFully'})

# Brand Management
class BrandListCreateView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]  
        elif self.request.method == 'POST':
            return [IsAdminorSuperuser()]  
        return super().get_permissions()
    
    def get(self,request):
        brand = Brand.objects.all()
        serializer = BrandSerializer(brand,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class BrandPostRetrieveUpdateDeleteView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]  
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminorSuperuser()]  
        return super().get_permissions()
    
    def get(self,request,pk):
        brand = Brand.objects.get(pk=pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)
    
    def put(self,request,pk):
        brand = Brand.objects.get(pk=pk)
        serializer = BrandSerializer(brand,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        brand = Brand.objects.get(pk=pk)
        brand.delete()
        return Response({'massage':'Delete SuccessFully'})
    
# Product Management  
class ProductListCreateView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]  
        elif self.request.method == 'POST':
            return [IsAdminorSuperuser()]  
        return super().get_permissions()
    
    def get(self, request):
        queryset = Product.objects.all()

        # Search
        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Filtering
        category_id = request.query_params.get('category', None)
        brand_id = request.query_params.get('brand', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        # Sorting
        sort_by = request.query_params.get('sort_by', None)
        if sort_by:
            if sort_by == 'price_asc':
                queryset = queryset.order_by('price')
            elif sort_by == 'price_desc':
                queryset = queryset.order_by('-price')
            elif sort_by == 'name_asc':
                queryset = queryset.order_by('name')
            elif sort_by == 'name_desc':
                queryset = queryset.order_by('-name')

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
     
    def post(self, request):
        data = request.data
        brand_id = Brand.objects.get(id=data['brand'])
        category_id = Categories.objects.get(id=data['categories'])
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(brand=brand_id, categories=category_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ProductPostRetrieveUpdateDeleteView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticatedOrReadOnly()]  
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminorSuperuser()]  
        return super().get_permissions()
    
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self,request,pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'massage':'Delete SuccessFully'})