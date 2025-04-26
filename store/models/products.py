from django.db import models 
from .category import Category 

class Products(models.Model): 
    name = models.CharField(max_length=60) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    description = models.CharField(max_length=250, default='', blank=True, null=True) 
    image = models.ImageField(upload_to='uploads/products/') 
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_new = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    
    # New fields for order functionality
    shipping_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=200.00,  # Default shipping fee in Ksh
        help_text="Shipping fee in Kenyan Shillings"
    )
    safaricom_till = models.CharField(
        max_length=10, 
        default='8600480',
        help_text="Safaricom Till Number for payments"
    )

    @property
    def discounted_price(self):
        """Calculate and return the discounted price if discount_percent is applied."""
        if self.discount_percent > 0:
            discount_amount = (self.price * self.discount_percent) / 100
            return round(self.price - discount_amount)
        return self.price

    @property
    def total_price(self):
        """Calculate total price including shipping"""
        return self.discounted_price + self.shipping_fee

    def __str__(self):
        return f"{self.name} - Ksh {self.discounted_price}"

    @staticmethod
    def get_products_by_id(ids): 
        return Products.objects.filter(id__in=ids) 

    @staticmethod
    def get_all_products(): 
        return Products.objects.all() 

    @staticmethod
    def get_all_products_by_categoryid(category_id): 
        if category_id: 
            return Products.objects.filter(category=category_id) 
        else: 
            return Products.get_all_products()

class ProductImage(models.Model):
    product = models.ForeignKey(Products, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/extra_images/')

    def __str__(self):
        return f"Image for {self.product.name}"