# from django.shortcuts import render
from django.conf import settings
from rest_framework import generics
# from rest_framework.response import Response
from django.http import JsonResponse
# from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .serializers import UserSerializer
from .models import CustomUser
from .utils import send_verification_email
from .utils import send_reset_password_email

import json


CustomUser = get_user_model()


# Create your views here.
def get_csrf_token(request):
    csrf_token = get_token(request)
    # return HttpResponse(csrf_token)
    return JsonResponse({'csrfToken': csrf_token})

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
    
    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(user)
        
        
def verify_email(request, uidb64, token):
    user_id = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(CustomUser, pk=user_id)
    
    if is_verification_expired(user.verification_expiry):
        user.delete()
        return HttpResponse('Verification link has expired and the account has been deleted.')
    
    if is_valid_token(user, token):
        user.is_verified = True
        user.save()
        return HttpResponse('Your email has been verified.')
    else:
        return HttpResponse('Verification link is invalid or has expired.')
    
    
def is_verification_expired(expiry_time):
    """
    Checks if the current time is past the given expiry time.

    Parameters:
    - expiry_time: A datetime object representing the expiration time of verification.

    Returns:
    - True if the current time is past the expiry time, otherwise False.
    """
    return timezone.now() > expiry_time


def is_valid_token(user, token):
    """
    Checks whether the token sent matches that of the user token

    Parameters:
    - user: A user object.
    - token: Token that came from the request

    Returns:
    - True if the tokens match, otherwise False.
    """
    return default_token_generator.check_token(user, token)    



@csrf_protect
def reset_password_with_email(request):
    csrf_token = request.META.get('HTTP_X_CSRFTOKEN', 'Not Found')
    print("CSRF Token received:", csrf_token)
    if request.method == 'POST':
        # CSRF-Token aus den Cookies oder dem Header extrahieren
        try:
            # JSON-Daten aus dem Body extrahieren
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            print("Show email: ", email)
            
            # Überprüfen, ob die E-Mail vorhanden ist
            if email:
                user = get_object_or_404(CustomUser, email=email)
                send_reset_password_email(user)
                return JsonResponse({'message': 'Password reset link has been sent to your email.'})
            else:
                return JsonResponse({'error': 'Email not provided.'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)