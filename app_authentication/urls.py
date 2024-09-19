from django.urls import path
from .views import UserCreateView, verify_email, reset_password_with_email, reset_password, user_login
from .test_mail import send_test_email

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='user-create'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
    path('login/', user_login, name='user_login'),
    path('send-reset-email/', reset_password_with_email, name='send-reset-email'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset-password'),
    path('send-test-email/', send_test_email, name='send_test_email'),
]