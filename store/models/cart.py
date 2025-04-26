# store/models/cart.py
from django.utils import timezone
from django.db import models
from store.models.customer import Customer

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart of {self.customer}"
