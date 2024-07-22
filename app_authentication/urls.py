from django.urls import path
from .views import UserCreateView, verify_email, reset_password_with_email, get_csrf_token

urlpatterns = [
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('registration/', UserCreateView.as_view(), name='user-create'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
    path('send-reset-email/', reset_password_with_email, name='send-reset-email'),
]