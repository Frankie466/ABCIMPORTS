from store.models import Cart, Customer  # Ensure Cart and Customer are imported

def cart_count_processor(request):
    count = 0
    if request.user.is_authenticated:
        try:
            # Query the Customer model to get the associated customer for the logged-in user
            customer = Customer.objects.get(user=request.user)
            count = Cart.objects.filter(customer=customer).count()  # Count the carts associated with the customer
        except Customer.DoesNotExist:
            count = 0  # Handle the case where the customer does not exist
    elif 'cart' in request.session:
        count = len(request.session['cart'])  # Handle session-based cart for non-authenticated users
    return {'cart_count': count}
