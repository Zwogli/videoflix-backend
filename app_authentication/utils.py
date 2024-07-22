from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.pk)) # Encode the pk(primäry key)
    verification_link = f"http://localhost:4200/verification/{user_id}/{token}/" #f"http://localhost:8000/auth/verify/{user_id}/{token}/"
    
    subject = 'Validierung der Email-Adresse für Videoflix'
    message = create_verification_message(user, verification_link)
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    
def create_verification_message(user, verification_link):
    return render_to_string('verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })
    
    
def send_reset_password_email(user):
    token = default_token_generator.make_token(user)
    user_id = urlsafe_base64_decode(force_bytes(user.pk))
    reset_link = f"{settings.Frontend_URL}/reset-password/{user_id}/{token}"
    
    subject = 'Passwort zurücksetzen für Videoflix'
    message = create_password_reset_message(user, reset_link)
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    

def create_password_reset_message(user, reset_link):
    return render_to_string('',{
        'user': user,
        'reset_link': reset_link,
    })