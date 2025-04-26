from django.shortcuts import render

def about_view(request):
    return render(request, 'store/about.html')

def contact_view(request):
    return render(request, 'store/contact.html')

def privacy_view(request):
    return render(request, 'store/privacy.html')

def terms_view(request):
    return render(request, 'store/terms.html')
