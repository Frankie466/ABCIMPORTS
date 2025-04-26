from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from store.models.products import Products
from store.models.orders import Order, OrderItem
from store.models.cart import Cart, CartItem
from store.models.customer import Customer
from store.forms import OrderForm
from datetime import datetime

@login_required
def product_list(request):
    products = Products.objects.all()
    for product in products:
        product.total_price = product.discounted_price + product.shipping_fee
    return render(request, 'store/product_list.html', {'products': products})

@login_required
@require_http_methods(["GET"])
def order_form(request, product_id):
    """Handle order form display (simplified version)"""
    product = get_object_or_404(Products, id=product_id)
    
    context = {
        'product': product,
        'form': OrderForm(initial={
            'product_id': product.id,
            'phone': request.user.customer.phone if hasattr(request.user, 'customer') else ''
        })
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('store/partials/order_form.html', context, request=request)
        return JsonResponse({
            'html': html,
            'product_name': product.name,
            'product_price': product.discounted_price
        })
    
    return render(request, 'store/orders.html', context)

@login_required
@require_http_methods(["POST"])
def process_order(request):
    """Skip actual processing and redirect to success page"""
    fake_order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('order_success', args=[fake_order_id])
        })
    else:
        return redirect('order_success', order_id=fake_order_id)

@login_required
def order_success(request):
    return render(request, 'store/order_success.html')


