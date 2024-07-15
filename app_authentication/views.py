from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from .serializers import UserSerializer
from .models import CustomUser
from .utils import send_verification_email


CustomUser = get_user_model()


# Create your views here.
def verify_email(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(CustomUser, pk=uid)
    if timezone.now() > user.verification_expiry:
        user.delete()
        return HttpResponse('Verification link has expired and the account has been deleted.')
    
    if default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return HttpResponse('Your email has been verified.')
    else:
        return HttpResponse('Verification link is invalid or has expired.')
    
    
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
    
    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(user)
    
    