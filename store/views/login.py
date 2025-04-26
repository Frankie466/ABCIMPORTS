from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from store.models.customer import Customer 
from django.views import View 

class Login(View): 
    return_url = None

    def get(self, request): 
        Login.return_url = request.GET.get('return_url') 
        return render(request, 'store/login.html') 

    def post(self, request): 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        error_message = None

        # Use Django's authenticate method to validate the user
        user = authenticate(request, username=email, password=password)

        if user is not None: 
            # Login the user
            auth_login(request, user)

            # Get the related Customer object
            try:
                customer = Customer.objects.get(user=user)
                request.session['customer'] = customer.id
            except Customer.DoesNotExist:
                error_message = "Customer not found"

            if Login.return_url: 
                return HttpResponseRedirect(Login.return_url) 
            else: 
                Login.return_url = None
                return redirect('homepage') 
        else: 
            error_message = 'Invalid Email or Password!!'

        print(email, password) 
        return render(request, 'store/login.html', {'error': error_message}) 


def logout(request): 
    auth_logout(request)
    return redirect('login')
