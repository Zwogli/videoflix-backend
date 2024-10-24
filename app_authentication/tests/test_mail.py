from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import BadHeaderError, send_mail
from unittest import mock


@mock.patch('app_authentication.tests.test_mail.send_mail')
def send_test_email(self, mock_send_mail):
    """
    Sends a test email to the specified recipient.
    """
    mock_send_mail.return_value = 1
    try:
        send_mail(
            'Test E-Mail',
            'Dies ist eine Test-E-Mail.',
            settings.DEFAULT_FROM_EMAIL,
            ['mathiaskohler@mail.de'],
            fail_silently=False,
        )
        return Response({'message': 'Test email has been sent.'}, status=status.HTTP_200_OK)
    except BadHeaderError:
        return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Error when sending the e-mail: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)