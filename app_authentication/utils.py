from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse

import json
import logging


logger = logging.getLogger('app_authentication')


def send_verification_email(user):
    """
    Sends a verification email to the specified user.

    Parameters:
    - user: The user object to whom the verification email will be sent.
    """
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.pk)) # Encode the pk (primäry key)
    logger.info(f"Generating verification email for user_id: {user_id}, token: {token}")
    verification_link = f"{settings.FRONTEND_URL}/verification/{user_id}/{token}/" 
    subject = 'Validation of the email address for Videoflix'
    message = create_verification_message(user, verification_link)
    
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.content_subtype = "html"  # Specify that the email content is HTML
    email.send()
    logger.info(f"Sent verification email to {user.email}")
    
    
def create_verification_message(user, verification_link):
    """
    Creates a verification email based on the user model and generates an individual verification link.
    """
    return render_to_string('verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })
    
    
def send_reset_password_email(user):
    """
    Generates an email to reset the user password.
    """
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{user_id}/{token}"
    
    subject = 'Passwort zurücksetzen für Videoflix'
    message = create_password_reset_message(user, reset_link)
    
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.content_subtype = "html"  # Specify that the email content is HTML
    email.send()
    

def create_password_reset_message(user, reset_link):
    """
    Creates an email to reset the user password
    """
    return render_to_string('reset_password_email.html',{
        'user': user,
        'reset_link': reset_link,
    })
    
    
def parse_request_body(request):
    """
    Parses the request body and returns it as a dictionary.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A dictionary representing the parsed JSON data.

    Raises:
    - ValueError: If the request body is not valid JSON.
    """
    return json.loads(request.body)


def extract_credentials(data):
    """
    Extracts email and password from the provided data dictionary.

    Parameters:
    - data: A dictionary containing user credentials.

    Returns:
    - A tuple containing the email and password.
    """
    email = data.get('email')
    password = data.get('password')
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
    

def generate_verification_token(user):
    """
    Generates a uidb64 and token for the user.

    :param user: The user instance.
    :return: A tuple of (uidb64, token).
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uidb64, token