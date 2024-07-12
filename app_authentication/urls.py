from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='user-create'),
]