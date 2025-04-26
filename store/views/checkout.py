from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from store.models.customer import Customer
from store.models.products import Products
from store.models.orders import Order

class CheckOut(View):
    # Display the checkout page with cart items
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated

        cart = request.session.get('cart')
        if not cart:
            return redirect('view_cart')  # Corrected to 'view_cart' if the cart is empty

        product_ids = list(cart.keys())
        products = Products.get_products_by_id(product_ids)

        # Calculate the total price of items in the cart
        total = sum([product.price * cart[str(product.id)] for product in products])

        context = {
            'cart_items': [{'product': product, 'quantity': cart[str(product.id)]} for product in products],
            'total': total,  # Total cost to be displayed on the checkout page
        }
        return render(request, 'store/checkout.html', context)

    # Handle the order placement process
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated

        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.user.customer  # Access the customer associated with the logged-in user
        cart = request.session.get('cart')

        if not cart:
            return redirect('view_cart')  # Redirect to view_cart if cart is empty

        products = Products.get_products_by_id(list(cart.keys()))

        # Create an order for each product in the cart
        for product in products:
            quantity = cart.get(str(product.id))
            if quantity:
                order = Order(
                    customer=customer,
                    product=product,
                    price=product.price,
                    address=address,
                    phone=phone,
                    quantity=quantity
                )
                order.save()

        # Clear the cart after placing the order
        request.session['cart'] = {}
        return redirect('orders')  # Redirect to the orders page after checkout
