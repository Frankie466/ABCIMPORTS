from django.contrib import admin
from django.urls import path
from store.views.home import Index, store, Category
from store.views.signup import Signup
from store.views.login import Login, logout
from store.views.cart import add_to_cart, remove_from_cart, update_cart, view_cart
from store.views.checkout import CheckOut
from store.views.orders import OrderView, process_order, order_success, order_error, order_form  # Added order_success
from store.views.search import SearchView
from store.views.product_detail import ProductDetail
from django.contrib.auth import views as auth_views
from store.views.category_detail import CategoryDetail
from store.views import info

urlpatterns = [
    # Basic routes
    path('', Index.as_view(), name='homepage'),
    path('store/', store, name='store'),
    
    # Authentication
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    
    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='store/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='store/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='store/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='store/password_reset_complete.html'), name='password_reset_complete'),
    
    # Cart functionality
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    
    # Order processing
    path('order/form/<int:product_id>/', order_form, name='order_form'),  # Display order form
    path('order/process/', process_order, name='process_order'),  # Process the form
    path('order/success/<int:order_id>/', order_success, name='order_success'),  # ✅ ADDED THIS
    path('order/error/', order_error, name='order_error'),
    
    # Checkout and orders
    path('check-out/', CheckOut.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),
    
    # Product browsing
    path('search/', SearchView.as_view(), name='search'),
    path('product/<int:id>/', ProductDetail.as_view(), name='product_detail'),
    path('category/<int:id>/', CategoryDetail.as_view(), name='category_detail'),

    # Info pages
    path('about/', info.about_view, name='about'),
    path('contact/', info.contact_view, name='contact'),
    path('privacy/', info.privacy_view, name='privacy'),
    path('terms/', info.terms_view, name='terms'),
]
