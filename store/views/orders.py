from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from store.models.products import Products
from store.models.orders import Order, OrderItem
from store.forms import OrderForm

class OrderView(View):
    @method_decorator(login_required)
    def get(self, request):
        orders = Order.objects.filter(customer=request.user.customer).order_by('-date_ordered')
        return render(request, 'store/partials/orders.html', {'orders': orders})

@login_required
def order_form(request, product_id):
    """Handle order form display with G4S payment arrangement"""
    product = get_object_or_404(Products, id=product_id)
    
    form = OrderForm(initial={
        'product_id': product.id,
        'phone': request.user.customer.phone,
        'address': 'G4S Pickup Station - Payment on Arrival'
    })
    
    # Make address field read-only
    form.fields['address'].widget.attrs['readonly'] = True
    
    context = {
        'product': product,
        'form': form,
        'payment_breakdown': {
            'shipping_fee': product.shipping_fee,
            'product_price': product.price,
            'total_now': product.shipping_fee,
            'total_later': product.price
        }
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('store/partials/order_form.html', context, request=request)
        return JsonResponse({'html': html})
    
    return render(request, 'store/partials/order_form.html', context)

@login_required
def order_error(request):
    return render(request, 'store/order_error.html')


@login_required
def process_order(request):
    """Process order with two-phase payment and redirect to success page"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    form = OrderForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    try:
        product = get_object_or_404(Products, id=form.cleaned_data['product_id'])
        
        # Create order with status 'Payment Pending'
        order = Order.objects.create(
            customer=request.user.customer,
            total=product.shipping_fee,  # Customer pays only shipping now
            county=form.cleaned_data['county'],
            town=form.cleaned_data['town'],
            address=form.cleaned_data['address'],
            phone=form.cleaned_data['phone'],
            status='Pending',
            notes=f"Pay Ksh {product.price} when collecting at G4S"
        )
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price,  # Full price (to be paid later)
            shipping_fee=product.shipping_fee,  # Paid now
        )
        
        # Redirect to the order success page
        return redirect('order_success', order_id=order.id)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

        # Create order with status 'Payment Pending'
        order = Order.objects.create(
            customer=request.user.customer,
            total=product.shipping_fee,  # Customer pays only shipping now
            county=form.cleaned_data['county'],
            town=form.cleaned_data['town'],
            address=form.cleaned_data['address'],
            phone=form.cleaned_data['phone'],
            status='Pending',
            notes=f"Pay Ksh {product.price} when collecting at G4S"
        )
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price,  # Full price (to be paid later)
            shipping_fee=product.shipping_fee,  # Paid now
           )
        
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('order_success', args=[order.id])
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    return render(request, 'store/order_success.html', {
        'order': order,
        'payment_info': {
            'paid_now': order.total,
            'pay_later': order.items.first().price if order.items.exists() else 0
        
        }
    })