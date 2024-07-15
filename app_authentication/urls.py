from django.urls import path
from .views import UserCreateView, verify_email

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='user-create'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
]