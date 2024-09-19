from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse

import json

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.pk)) # Encode the pk(primäry key)
    verification_link = f"{settings.FRONTEND_URL}/verification/{user_id}/{token}/" #f"http://localhost:8000/auth/verify/{user_id}/{token}/"
    
    subject = 'Validierung der Email-Adresse für Videoflix'
    message = create_verification_message(user, verification_link)
    
    # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.content_subtype = "html"  # Specify that the email content is HTML
    email.send()
    
    
def create_verification_message(user, verification_link):
    return render_to_string('verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })
    
    
def send_reset_password_email(user):
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{user_id}/{token}"
    
    subject = 'Passwort zurücksetzen für Videoflix'
    message = create_password_reset_message(user, reset_link)
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    

def create_password_reset_message(user, reset_link):
    return render_to_string('reset_password_email.html',{
        'user': user,
        'reset_link': reset_link,
    })
    
    
def parse_request_body(request):
    return json.loads(request.body)


def extract_credentials(data):
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