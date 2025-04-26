# views/search.py
from django.shortcuts import render
from store.models.products import Products
from django.views import View

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        products = Products.objects.filter(name__icontains=query)
        return render(request, 'store/search.html', {'products': products, 'query': query})
