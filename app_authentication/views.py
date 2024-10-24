from django.conf import settings
from rest_framework import generics, status
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from .models import CustomUser
from . import utils

import json
import logging


logger = logging.getLogger('app_authentication')
CustomUser = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
    def perform_create(self, serializer):
        user = serializer.save()
        utils.send_verification_email(user)
        

@api_view(['GET'])        
def verify_email(request, uidb64, token):
    """
    Verifies the user's email using the provided UID and token.

    :param request: The HTTP request object.
    :param uidb64: Base64 encoded user ID.
    :param token: Token sent in the verification email.
    :return: Response indicating the result of the verification process.
    """
    logger.debug(f"Verifying email for uidb64: {uidb64} with token: {token}")
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(CustomUser, pk=user_id)
        logger.debug(f"User found: {user.user_name}")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        logger.error("Invalid user ID format.")
        return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if is_verification_expired(user.verification_expiry):
        logger.warning(f"Verification expired for user: {user.user_name}")
        return handle_expired_verification(user)
    
    if is_valid_token(user, token):
        user.is_verified = True
        user.save()
        logger.info(f"User {user.user_name} has been verified successfully.")
        return Response({'message': 'Your email has been verified.'}, status=status.HTTP_200_OK)
    else:
        logger.warning(f"Invalid token provided for user {user.user_name}.")
        return Response({'error': 'Verification link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
def handle_expired_verification(user):
    user.delete()
    return Response({'message': 'Verification link has expired and the account has been deleted.'}, status=status.HTTP_410_GONE)    
    
    
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


@api_view(['POST'])
def user_login(request):
    """
    Handles user login via POST request with email and password.

    :param request: The HTTP request object containing the user's credentials.
    :return: Response with the authentication token or error message.
    """
    if request.method == "POST":
        try:
            data = utils.parse_request_body(request)
            email, password = utils.extract_credentials(data)
        
            if not email:
                return utils.missing_field_response('email')
            if not password:
                return utils.missing_field_response('password')
            
            user = authenticate(request, email=email, password=password)
            
            if user is None:
                return utils.invalid_credentials_response()
            if not user.is_verified:
                return Response({'error': 'Email not verified.'}, status=status.HTTP_403_FORBIDDEN)
            
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON.'}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



def reset_password_with_email(request):
    """
    Resets the user's password if the token is valid.

    :param request: The HTTP request object containing the new password.
    :param uidb64: Base64 encoded user ID.
    :param token: Token for password reset validation.
    :return: Response indicating the result of the password reset process.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            
            if email:
                user = get_object_or_404(CustomUser, email=email)
                utils.send_reset_password_email(user)
                return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Email not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def reset_password(request, uidb64, token):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_password = data.get('password')
            
            if not new_password:
                return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_id = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = get_object_or_404(CustomUser, pk=user_id)
            
            if default_token_generator.check_token(user, token):
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)