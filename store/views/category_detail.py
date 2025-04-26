# store/views/category_detail.py
from django.shortcuts import render, get_object_or_404
from django.views import View
from store.models.category import Category  # Import the correct Category model
from store.models.products import Products  # Import the correct Products model

class CategoryDetail(View):
    def get(self, request, id):
        # Fetch the category by ID
        category = get_object_or_404(Category, id=id)
        
        # Fetch all products in this category
        products_in_category = Products.objects.filter(category=category)
        
        return render(request, 'store/category_detail.html', {
            'category': category,
            'products': products_in_category,
        })
