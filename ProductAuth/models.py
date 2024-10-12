from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    discription = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_photo' ,null=True, blank=True)
    
    def __str__(self):
        return self.name