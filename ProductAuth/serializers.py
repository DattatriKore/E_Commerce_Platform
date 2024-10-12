from rest_framework import serializers
from .models import Categories,Brand,Product

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id','name']
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id','name']
        
class ProductSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id','name','discription','categories','brand','image','price']
        
# from rest_framework import serializers
# from .models import Product, Brand

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'categories', 'brand', 'price']

#     def create(self, validated_data):
#         brand_id = validated_data.get('brand')
#         if not brand_id:
#             raise serializers.ValidationError("Brand ID is required")
        
#         try:
#             brand = Brand.objects.get(id=brand_id)
#         except Brand.DoesNotExist:
#             raise serializers.ValidationError("Brand does not exist")

#         validated_data['brand'] = brand
#         return super().create(validated_data)