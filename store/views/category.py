from django.shortcuts import render
from store.models import category

def display_categories(request):
    categories = category.object.all()
    return render(request, 'home.html',{'categories'})