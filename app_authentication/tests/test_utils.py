import pytest
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import json
from ..models import CustomUser
from ..utils import (
    send_verification_email,
    send_reset_password_email,
    parse_request_body,
    extract_credentials,
    missing_field_response,
    invalid_credentials_response,
    success_response,
    generate_verification_token,
)

@pytest.mark.django_db
class TestUtils:

    @pytest.fixture
    def user(self):
        """Create a sample user for testing."""
        return CustomUser.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )


    def test_send_verification_email(self, user):
        """Test if verification email is sent."""
        send_verification_email(user)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Validation of the email address for Videoflix'
        assert 'test@example.com' in mail.outbox[0].to


    def test_send_reset_password_email(self, user):
        """Test if reset password email is sent."""
        send_reset_password_email(user)
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Passwort zurücksetzen für Videoflix'
        assert 'test@example.com' in mail.outbox[0].to


    def test_parse_request_body(self):
        """Test parsing a valid JSON request body."""
        class MockRequest:
            body = b'{"email": "test@example.com", "password": "testpassword"}'

        request = MockRequest()
        data = parse_request_body(request)
        assert data == {"email": "test@example.com", "password": "testpassword"}


    def test_parse_request_body_invalid_json(self):
        """Test parsing an invalid JSON request body raises ValueError."""
        class MockRequest:
            body = b'invalid json'

        request = MockRequest()
        with pytest.raises(ValueError):
            parse_request_body(request)


    def test_extract_credentials(self):
        """Test extracting email and password from data."""
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        email, password = extract_credentials(data)
        assert email == 'test@example.com'
        assert password == 'testpassword'


    def test_missing_field_response(self): 
        """Test missing field response.""" 
        response = missing_field_response('email')

        # Ändere hier die erwartete Antwort
        expected_response = {
            'error': 'Email not provided.'  # Nur die Fehlernachricht
        }

        # Verwende die Hilfsfunktion
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert response_data == expected_response


    def test_invalid_credentials_response(self):
        """Test invalid credentials response.""" 
        response = invalid_credentials_response()

        # Ändere hier die erwartete Antwort
        expected_response = {
            'error': 'Invalid email or password.'  # Nur die Fehlernachricht
        }

        # Verwende die Hilfsfunktion
        assert response.status_code == 401
        response_data = json.loads(response.content)
        assert response_data == expected_response


    def test_success_response(self, user):
        """Test success response for user login.""" 
        response = success_response(user)
        expected_response = {
            'success': 'User logged in successfully.',
            'user_id': user.id
        }

        # Verwende die Hilfsfunktion
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data == expected_response


    def test_generate_verification_token(self, user):
        """Test generating a verification token."""
        uidb64, token = generate_verification_token(user)
        assert uidb64 == urlsafe_base64_encode(force_bytes(user.pk))
        assert token == default_token_generator.make_token(user)