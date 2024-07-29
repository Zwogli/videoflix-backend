from django.urls import path
from .views import UserCreateView, verify_email, reset_password_with_email, reset_password

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='user-create'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
    path('send-reset-email/', reset_password_with_email, name='send-reset-email'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset-password'),
]