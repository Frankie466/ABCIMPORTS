# store/models/customer.py
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User model
    phone = models.CharField(max_length=10)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(user__email=email)  # Get customer by linked User's email
        except Customer.DoesNotExist:
            return False

    def isExists(self):
        return Customer.objects.filter(user__email=self.user.email).exists()
