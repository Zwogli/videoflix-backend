import pytest
from django.urls import reverse
from django.core import mail

from ..models import CustomUser
from ..utils import send_verification_email
from ..serializers import UserSerializer


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


    def test_user_creation(self, user):
        """Test if the user is created correctly."""
        assert CustomUser.objects.count() == 1
        assert user.email == 'test@example.com'


    def test_send_verification_email(self, user):
        """Test if verification email is sent."""
        send_verification_email(user)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Validation of the email address for Videoflix'
        assert 'test@example.com' in mail.outbox[0].to


    def test_registration_view(self, client):
        """Test if registration view works."""
        response = client.post(reverse('user-create'), {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
        })
        assert response.status_code == 201  # Assuming 201 Created
        assert CustomUser.objects.count() == 1  # Check if the user was created
        
        
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
