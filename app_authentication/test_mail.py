from django.core.mail import send_mail
from django.http import HttpResponse

def send_test_email(request):
    send_mail('Test E-Mail', 'Dies ist eine Test-E-Mail.', 'videoflix@mathias-kohler.de', ['mathiaskohler@mail.de'])
    return HttpResponse('Test E-Mail wurde gesendet.')

from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import BadHeaderError

def send_test_email(request):
    try:
        send_mail(
            'Test E-Mail',
            'Dies ist eine Test-E-Mail.',
            settings.DEFAULT_FROM_EMAIL,
            ['mathiaskohler@mail.de'],
            fail_silently=False,
        )
        return HttpResponse('Test E-Mail wurde gesendet.')
    except BadHeaderError:
        return HttpResponse('Ungültiger Header gefunden.')
    except Exception as e:
        return HttpResponse(f'Fehler beim Senden der E-Mail: {str(e)}')