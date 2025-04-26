from django.shortcuts import redirect
from django.urls import reverse

def auth_middleware(get_response):
    def middleware(request):
        # For now, ignore authentication checks
        # Just call the view without any redirection
        response = get_response(request)
        return response

    return middleware
