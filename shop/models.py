from django.db import models

# Importing necessary module

# Product Model
class Product(models.Model):
    # Fields of the Product model
    name = models.CharField(max_length=255) 
    description = models.TextField()  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    image_url = models.ImageField(upload_to='products/')  

    # String representation of the Product model
    def __str__(self):
        return self.name
