from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='user-create'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify-email'),
]