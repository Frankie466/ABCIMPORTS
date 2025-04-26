# store/admin.py
from django.contrib import admin
from store.models.products import Products, ProductImage
from store.models.category import Category
from store.models.customer import Customer
from store.models.orders import Order

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra blank images to display

# Admin for Products with ProductImageInline
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_new', 'discount_percent', 'rating')
    inlines = [ProductImageInline]

# Register other models as usual
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
