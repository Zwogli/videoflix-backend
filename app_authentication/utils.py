from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"http://localhost:8000/auth/verify/{uid}/{token}/"
    
    subject = 'Verify your email address'
    message = render_to_string('verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])