from django.shortcuts import render, redirect, get_object_or_404
from store.models.products import Products
from store.models.cart import Cart
from store.models.cart_item import CartItem
from store.models.customer import Customer


def get_cart_item_count(request):
    """Helper function to get total item count in cart."""
    if request.user.is_authenticated:
        try:
            customer = get_object_or_404(Customer, user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            return CartItem.objects.filter(cart=cart).count()
        except Customer.DoesNotExist:
            return 0
    else:
        # For non-authenticated users, get the cart from session
        return len(request.session.get('cart_items', []))


def add_to_cart(request, product_id):
    """Add an item to the cart."""
    product = get_object_or_404(Products, id=product_id)
    
    if request.user.is_authenticated:
        try:
            customer = get_object_or_404(Customer, user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
            cart_item.save()
        except Customer.DoesNotExist:
            return redirect('login')  # Redirect to login if customer does not exist
    else:
        # Handle cart for non-logged-in users using session
        cart_items = request.session.get('cart_items', [])
        
        # Check if the product already exists in the cart
        existing_item = next((item for item in cart_items if item['product_id'] == product.id), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart_items.append({'product_id': product.id, 'quantity': 1})
        
        # Save the updated cart in session
        request.session['cart_items'] = cart_items

    # Calculate the total number of items in the cart
    total_items = get_cart_item_count(request)

    # Store message in session
    request.session['cart_message'] = 'Item added to cart!'

    # Return a redirect
    return redirect('homepage')  # Redirect to the home page or the page where they were before 


def home(request):
    if 'cart_message' in request.session:
        cart_message = request.session['cart_message']
        del request.session['cart_message']
    else:
        cart_message = None

    return render(request, 'store/home.html', {'cart_message': cart_message})


def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    if request.user.is_authenticated:
        try:
            customer = get_object_or_404(Customer, user=request.user)
            cart_item = get_object_or_404(CartItem, id=item_id)
            cart_item.delete()
        except Customer.DoesNotExist:
            return redirect('login')  # Redirect to login if customer does not exist
    else:
        # For non-authenticated users, remove from session cart
        cart_items = request.session.get('cart_items', [])
        cart_items = [item for item in cart_items if item['product_id'] != int(item_id)]
        request.session['cart_items'] = cart_items
    
    return redirect('view_cart')


def update_cart(request, item_id):
    """Update the quantity of an item in the cart."""
    if request.user.is_authenticated:
        try:
            customer = get_object_or_404(Customer, user=request.user)
            cart_item = get_object_or_404(CartItem, id=item_id)

            if request.method == 'POST':
                quantity = int(request.POST.get('quantity', 1))
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
        except Customer.DoesNotExist:
            return redirect('login')  # Redirect to login if customer does not exist
    else:
        # For non-authenticated users, update session cart
        cart_items = request.session.get('cart_items', [])
        for item in cart_items:
            if item['product_id'] == int(item_id):
                item['quantity'] = int(request.POST.get('quantity', 1))
                if item['quantity'] <= 0:
                    cart_items.remove(item)
        request.session['cart_items'] = cart_items

    return redirect('view_cart')


def view_cart(request):
    """Display the cart."""
    cart_items = []
    total = 0
    
    if request.user.is_authenticated:
        try:
            customer = get_object_or_404(Customer, user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
            cart_items = CartItem.objects.filter(cart=cart)
            total = sum(item.get_total_price() for item in cart_items)
        except Customer.DoesNotExist:
            return redirect('login')  # Redirect to login if customer does not exist
    else:
        # For non-authenticated users, fetch cart items from session
        cart_items_data = request.session.get('cart_items', [])
        for item_data in cart_items_data:
            product = get_object_or_404(Products, id=item_data['product_id'])
            cart_item = {'product': product, 'quantity': item_data['quantity'], 'get_total_price': product.price * item_data['quantity']}
            cart_items.append(cart_item)
            total += cart_item['get_total_price']

    # Get total item count in the cart
    cart_item_count = get_cart_item_count(request)

    # Check if the cart is empty
    show_start_shopping = len(cart_items) == 0
    cart_message = "Your cart is empty! Explore our categories and start shopping."

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_item_count': cart_item_count,
        'show_start_shopping': show_start_shopping,
        'cart_message': cart_message
    })
