from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(CustomUser):
    class Meta:
        model = CustomUser
        fields = '__all__'