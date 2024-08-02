from django.conf import settings
from rest_framework import generics
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer
from .models import CustomUser
from .utils import send_verification_email
from .utils import send_reset_password_email

import json


CustomUser = get_user_model()


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


def user_login(request):
    """
    Handles user login via POST request with email and password.
    """
    if request.method == "POST":
        try:
            data = parse_request_body(request)
            email, passwort = extract_credentials(data)
        
            if not email:
                return missing_field_response('email')
            
            if not passwort:
                return missing_field_response('email')
            
            user = authenticate(request, email=email, password=passwort)
            
            if user is None:
                return invalid_credentials_response()
            
            login(request, user)
            return success_response(user)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
    
def parse_request_body(request):
    return json.loads(request.body)


def extract_credentials(data):
    email = data.get('email')
    password = data.get('passwort')
    return email, password


def missing_field_response(field_name):
    return JsonResponse({'error': f'{field_name.capitalize()} not provided.'}, status=400)


def invalid_credentials_response():
    return JsonResponse({'error': 'Invalid email or password.'}, status=401)


def success_response(user):
    return JsonResponse({
        'success': 'User logged in successfully.',
        'user_id': user.id
    })


def reset_password_with_email(request):
    print('Hello World')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            print("Show email: ", email)
            
            if email:
                user = get_object_or_404(CustomUser, email=email)
                send_reset_password_email(user)
                return JsonResponse({'message': 'Password reset link has been sent to your email.'})
            else:
                return JsonResponse({'error': 'Email not provided.'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def reset_password(request, uidb64, token):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_password = data.get('password')
            
            if not new_password:
                return JsonResponse({'error': 'Password is required.'}, status=400)
            
            try:
                user_id = urlsafe_base64_decode(uidb64).decode('utf-8')
            except (TypeError, ValueError, OverflowError):
                return JsonResponse({'error': 'Invalid user ID.'}, status=400)
            
            user = get_object_or_404(CustomUser, pk=user_id)
            
            if default_token_generator.check_token(user, token):
                user.password = make_password(new_password)
                user.save()
                return JsonResponse({'message': 'Password has been reset successfully.'})
            else:
                return JsonResponse({'error': 'Invalid token or user ID.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)