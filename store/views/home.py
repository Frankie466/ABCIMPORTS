from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models.products import Products
from store.models.category import Category
from store.models.products import ProductImage  # Import the ProductImage model
from django.views import View

class Index(View):
    
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        # Fetch products and categories
        products = Products.get_all_products()
        categories = Category.get_all_categories()

        # Add multiple images to each product in the context
        products_with_images = []
        for product in products:
            product_images = ProductImage.objects.filter(product=product)
            products_with_images.append({
                'product': product,
                'images': product_images
            })

        # Prepare the context with products (including images) and categories
        data = {
            'products_with_images': products_with_images,
            'categories': categories,
        }

        return render(request, 'store/home.html', data)


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    # Add multiple images to each product in the store view as well
    products_with_images = []
    for product in products:
        product_images = ProductImage.objects.filter(product=product)
        products_with_images.append({
            'product': product,
            'images': product_images
        })

    data = {
        'products_with_images': products_with_images,
        'categories': categories,
    }

    print('you are : ', request.session.get('email'))
    return render(request, 'store/home.html', data)
