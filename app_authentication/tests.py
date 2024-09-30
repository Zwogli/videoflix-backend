import pytest
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from .models import CustomUser
from .utils import send_verification_email
from .serializers import UserSerializer
from . import utils

@pytest.mark.django_db
class TestCustomUser:

    @pytest.fixture
    def user(self):
        """Create a sample user for testing."""
        return CustomUser.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )


    def test_user_creation_view(self, client):
        """Test if the user creation view works."""
        response = client.post(reverse('user-create'), {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
        })
        assert response.status_code == 201  # Assuming 201 Created
        assert CustomUser.objects.count() == 1  # Check if the user was created
        assert CustomUser.objects.get(email='newuser@example.com').is_verified is False  # Check if the user is not verified yet


    def test_verify_email_success(self, client, user):
        """Test successful email verification."""
        # Assuming you have a utility to generate valid uidb64 and token
        uidb64, token = utils.generate_verification_token(user)  # This should be a function that you implement
        response = client.get(reverse('verify-email', kwargs={'uidb64': uidb64, 'token': token}))
        assert response.status_code == 200
        assert response.data['message'] == 'Your email has been verified.'
        user.refresh_from_db()  # Refresh the user instance from the database
        assert user.is_verified is True  # Check if the user is now verified


    def test_verify_email_invalid_token(self, client, user):
        """Test email verification with an invalid token."""
        uidb64 = 'invalid_uidb64'
        token = 'invalid_token'
        response = client.get(reverse('verify-email', kwargs={'uidb64': uidb64, 'token': token}))
        assert response.status_code == 400
        assert response.data['error'] == 'Verification link is invalid or has expired.'

    def test_user_login_success(self, client, user):
        """Test successful user login."""
        response = client.post(reverse('user_login'), {
            'email': 'test@example.com',
            'password': 'testpassword',
        })
        assert response.status_code == 200
        assert 'token' in response.data  # Ensure that a token is returned

    def test_user_login_not_verified(self, client, user):
        """Test login for a user whose email is not verified."""
        response = client.post(reverse('user_login'), {
            'email': 'test@example.com',
            'password': 'testpassword',
        })
        assert response.status_code == 403
        assert response.data['error'] == 'Email not verified.'

    def test_user_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post(reverse('user_login'), {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword',
        })
        assert response.status_code == 401  # Unauthorized
        assert response.data['error'] == 'Invalid credentials.'
        
        
    def test_user_serializer_valid(self):
        """Test if user serializer works with valid data."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()  # Serializer should be valid


    def test_user_serializer_invalid(self):
        """Test if user serializer fails with invalid data."""
        data = {
            'email': 'invalid-email',
            'password': 'newpassword',
            'first_name': '',
            'last_name': 'User',
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()  # Serializer should be invalid