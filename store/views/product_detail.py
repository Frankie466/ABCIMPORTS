from django.shortcuts import render, get_object_or_404
from django.views import View
from store.models.products import Products, ProductImage  # Import the Product and ProductImage models

class ProductDetail(View):
    def get(self, request, id):
        # Retrieve the product by ID and related images
        product = get_object_or_404(Products, id=id)
        images = product.images.all()  # Retrieve additional images
        similar_products = Products.objects.filter(category=product.category).exclude(id=product.id)[:4]  # Get related products

        # Pass data to the template
        context = {
            'product': product,
            'images': images,
            'similar_products': similar_products,
            # Add any other details like ratings, reviews, etc.
        }
        return render(request, 'store/product_detail.html', context)
