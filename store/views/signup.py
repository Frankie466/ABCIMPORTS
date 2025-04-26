from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from store.models.customer import Customer
from django.views import View

class Signup(View):
    def get(self, request):
        return render(request, 'store/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        # Create a Customer instance without email and password
        customer = Customer(
            phone=phone
        )

        error_message = self.validateCustomer(customer, email, password)

        if not error_message:
            # Create the User object first
            user = User.objects.create_user(
                username=email,  # use email as the username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Link the Customer to the User
            customer.user = user  # Assign the User to the Customer
            customer.register()    # Now save the Customer

            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'store/signup.html', data)

    def validateCustomer(self, customer, email, password):
        error_message = None
        if not email:
            error_message = "Email is required."
        elif len(email) < 5:
            error_message = "Email must be at least 5 characters long."
        elif len(password) < 5:
            error_message = "Password must be at least 5 characters long."
        elif User.objects.filter(email=email).exists():
            error_message = "Email already registered."
        elif len(customer.phone) != 10:
            error_message = "Phone number must be 10 digits long."

        return error_message
