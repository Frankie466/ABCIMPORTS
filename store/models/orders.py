# store/models/orders.py
from django.db import models
from django.utils import timezone
from .customer import Customer
from .products import Products

class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)   
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    
    # Delivery Information
    county = models.CharField(max_length=100, default='Nairobi')
    town = models.CharField(max_length=100, default='Nairobi')
    address = models.TextField(default='Address not specified')
    phone = models.CharField(max_length=10, default='0712345678')
    alt_phone = models.CharField(max_length=15, blank=True, null=True)
   
       # Add the notes field
    notes = models.TextField(blank=True, null=True)  # Optional notes field
    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def total_price(self):
        return (self.price * self.quantity) + self.shipping_fee
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"