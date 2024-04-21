from django.db import models
from urllib.parse import quote_plus 

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)

    def get_dummy_image_url(self):
        """
        Always generates a URL for a dummy image using the product's name as the text.
        """
        safe_product_name = quote_plus(self.name)
        return f"https://dummyimage.com/600x400/cccccc/000000.png&text={safe_product_name}"